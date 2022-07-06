import pandas as pd
import time
import matplotlib.pyplot as plt

initTime = time.time()

df = pd.read_csv("./data/0_Boxing_full.csv",encoding='utf-8-sig')

# seperate date into day, month and year
df[["day", "month", "year"]] = df["release_date"].str.split(" ", expand = True)
# change month to numerical value
def monthConvert(month):
	value = 0
	if month == 'Jan,':
		value = 1
	elif month == 'Feb,':
		value = 2
	elif month == 'Mar,':
		value = 3
	elif month == 'Apr,':
		value = 4
	elif month == 'May,':
		value = 5
	elif month == 'Jun,':
		value = 6
	elif month == 'Jul,':
		value = 7
	elif month == 'Aug,':
		value = 8
	elif month == 'Sep,':
		value = 9
	elif month == 'Oct,':
		value = 10
	elif month == 'Nov,':
		value = 11
	else:
		value = 12
	return value

df['month'] = df['month'].map(lambda x:monthConvert(x))

# convert dateformat
df['release_date'] = pd.to_datetime(df['release_date'])
df = df.sort_values(by="release_date")

# https://stackoverflow.com/questions/48739374/pandas-plot-cumulative-sum-of-counters-over-time
# create graph of total amount of games released
dfAmount = df[['release_date']].copy()
dfAmount['total'] = 1
dfAmount.set_index('release_date',inplace=True)
dfAmount.sort_index().cumsum().plot(color="green")

# plot
plt.axvline('2019-07-24', color='red')
plt.xlabel('Release Date')
plt.ylabel('Total')
plt.title('Boxing')
plt.savefig('./plots/plot.png')

dfScore = df[['release_date','score_rank','positive','negative']].copy()

# calculate score rank
def calculate_score(pos,neg):
	intpost,intneg  = int(pos),int(neg)
	return float((intpost/(intpost+intneg))*100)

dfScore['pos_neg'] = dfScore['positive'].astype(str)+"\t"+dfScore['negative'].astype(str)
dfScore['score_rank'] = dfScore['pos_neg'].map(lambda x:calculate_score(x.split('\t')[0],x.split('\t')[1]))

score = dfScore['score_rank']

dfScore['score_mean'] = dfScore['score_rank'].rolling(5).mean()
dfScore = dfScore[['release_date','score_mean']]

dfScore.set_index('release_date',inplace=True)
plt.clf()
dfScore['score_mean'].plot(color="orange")

plt.legend(["Mean score"],loc=0)

# plot
plt.axvline('2019-07-24', color='red')
plt.xlabel('Release Date')
plt.ylabel('Score')
plt.title('Boxing Score')
plt.savefig('./plots/plotscore.png')

total = time.time()
print(f"Total time: \t {total - initTime}")