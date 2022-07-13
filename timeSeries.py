import pandas as pd
import time
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import math 
import os
import dataAmount

initTime = time.time()

# files that have less than 100 entires
tooShort = dataAmount.main()

dataFolder = './data/'
directory = os.fsencode(dataFolder)

# loop through all datasets
for file in os.listdir(directory):	
	start = time.time()

	fileName = os.fsdecode(file)

	if (fileName.endswith('.csv') and fileName not in tooShort):

		print(f"Start with: \t {fileName}")

		df = pd.read_csv('./data/' + fileName,encoding='utf-8-sig')
		genre = fileName.split('_')[1]

		# colors for graph
		color1 = "blue"
		color2 = "red"
		color3 = 'green'
		color4 = "grey"

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

		# create graph of total amount of games, mean score, mean price
		dfCopy = df[['release_date','score_rank','positive','negative','price']].copy()

		# calculate a score rank based on positive and negative
		def calculate_score(pos,neg):
			intpost,intneg  = int(pos),int(neg)
			# no results stop division by zero
			if(intpost == 0 or intneg == 0):
				return 0
			return int((intpost/(intpost+intneg))*100)

		dfCopy.set_index('release_date',inplace=True)
		# https://stackoverflow.com/questions/48739374/pandas-plot-cumulative-sum-of-counters-over-time
		# total amount of games released
		dfCopy['total'] = 1
		dfCopy['cumsum'] = dfCopy['total'].sort_index().cumsum()
		# Mean scores of the game
		dfCopy['pos_neg'] = dfCopy['positive'].astype(str)+"\t"+dfCopy['negative'].astype(str)
		dfCopy['score_rank'] = dfCopy['pos_neg'].map(lambda x:calculate_score(x.split('\t')[0],x.split('\t')[1]))
		dfCopy['score_mean'] = dfCopy['score_rank'].rolling(10).mean()
		# Mean price of the game
		dfCopy['price'] = dfCopy['price']/10 
		dfCopy['price_mean'] = dfCopy['price'].rolling(10).mean()

		# roundup to nearest 100th for y-limit
		def roundup(x):
			return int(math.ceil(x / 100.0)) * 100
		max = roundup(dfCopy['price_mean'].max())

		# plot
		fig,ax = plt.subplots()
		fig.subplots_adjust(right=0.75)

		# for creating multiple y axis
		twin1 = ax.twinx()
		twin2= ax.twinx()

		twin2.spines.right.set_position(("axes", 1.2))

		labels = ['Total Games','Mean Score','Mean Price','Start Corona']
		# total games line
		ln1 = ax.plot(dfCopy['cumsum'],color=color1,label=labels[0])
		ax.set_xlabel('Release Date')
		ax.set_ylabel(labels[0],color=color1)

		# mean score and price lines
		ln2 = twin1.plot(dfCopy['score_mean'],color=color2,label=labels[1])
		ln3 = twin2.plot(dfCopy['price_mean'],color=color3,label=labels[2])

		lns = ln1+ln2+ln3

		# Coronadate line
		coronaDate = '2019-12-01'
		ln4 = ax.axvline(pd.to_datetime(coronaDate), color=color4,label=labels[3])
		lns.append(ln4)

		ax.legend(handles=lns,loc=0)
		ax.grid()
		twin1.set_ylim(0,100)
		twin1.set_ylabel(labels[1], color=color2)
		twin2.set_ylim(0,max)
		twin2.set_ylabel(labels[2], color=color3)

		plt.title(f'{genre} Score')
		plt.savefig(f'./plots/{genre}.png')
		plt.close()
		done = time.time()

		print(f"Total time: \t {done - start}")
		print("===========================")

total = time.time()
print(f"Total time: \t {total - initTime}")