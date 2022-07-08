import pandas as pd
import time
from matplotlib import pyplot as plt

initTime = time.time()

df = pd.read_csv("./data/0_Boxing_full.csv",encoding='utf-8-sig')

# colors for graph
color1 = "blue"
color2 = "orange"
color3 = "grey"

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
dfAmount.set_index('release_date',inplace=True)
dfAmount['total'] = 1
dfAmount['cumsum'] = dfAmount['total'].sort_index().cumsum()

fig,ax = plt.subplots()
ax = dfAmount['cumsum'].plot(color=color1,label="Total")
ax.legend('Total',loc=0)

# plot
# plt.axvline('2019-07-24', color='red')
ax.set_xlabel('Release Date')
ax.set_ylabel('Total',color=color1)
ax.legend(loc=0)
dfScore = df[['release_date','score_rank','positive','negative']].copy()

# ----------------------------------------------------------------------------
# create graph of mean score

# calculate a score rank based on positive and negative
def calculate_score(pos,neg):
	intpost,intneg  = int(pos),int(neg)
	return int((intpost/(intpost+intneg))*100)

dfScore['pos_neg'] = dfScore['positive'].astype(str)+"\t"+dfScore['negative'].astype(str)
dfScore['score_rank'] = dfScore['pos_neg'].map(lambda x:calculate_score(x.split('\t')[0],x.split('\t')[1]))
dfScore['score_mean'] = dfScore['score_rank'].rolling(10).mean()

dfScore.set_index('release_date',inplace=True)
ax2 = ax.twinx()
ax2 = dfScore['score_mean'].plot(color=color2,label="Mean Score")
ax2.set_ylabel("Mean score", color=color2)
ax2.legend(["Mean score"],loc=1)
ax2.set_ylim(0,100)

# plot
coronaDate = '2019-12-01'
ax2.axvline(coronaDate, color=color3,label="Start Corona")
ax2.legend(loc = 4)
plt.title('Boxing Score')
plt.savefig('./plots/plotscore.png')

total = time.time()
print(f"Total time: \t {total - initTime}")