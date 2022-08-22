import pandas as pd
import time
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import math 
import os
import dataExlude
import numpy as np

initTime = time.time()

# files that have less than 100 entires
# tooShort = dataExlude.main()

dataFolder = './data/'
directory = os.fsencode(dataFolder)

# colors for graph
color1 = "blue"
color2 = "red"
color3 = 'green'

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

# calculate a score rank based on positive and negative
def calculate_score(pos,neg):
	intpost,intneg  = int(pos),int(neg)
	# no results stop division by zero
	if(intpost == 0 or intneg == 0):
		return 0
	return int((intpost/(intpost+intneg))*100)

# roundup to nearest 10th for y-limit
def roundup(x):
	return int(math.ceil(x / 10.0)) * 10

# loop through all datasets
for file in os.listdir(directory):	
	start = time.time()

	fileName = os.fsdecode(file)

	# if (fileName.endswith('.csv') and fileName not in tooShort):
	if (fileName == '0_Pinball_full.csv'):
	# if (fileName == '58_Female Protagonist_full.csv'):

		print(f"Start with: \t {fileName}")

		df = pd.read_csv('./data/' + fileName,encoding='utf-8-sig')
		genre = fileName.split('_')[1]

		# seperate date into day, month and year
		df[["day", "month", "year"]] = df["release_date"].str.split(" ", expand = True)
		# change month to numerical value
		df['month'] = df['month'].map(lambda x:monthConvert(x))

		# convert dateformat
		df['release_date'] = pd.to_datetime(df['release_date'])
		df = df.sort_values(by="release_date")

		# create graph of total amount of games, mean score, mean price
		dfCopy = df[['release_date','score_rank','positive','negative','price','year']].copy()

# Regression for genre -------------------------------------------------------------------
		# convert value counts to a dataframe
		dfValuesCount = pd.DataFrame(dfCopy['release_date'].value_counts())
		dfValuesCount = dfValuesCount.reset_index()
		dfValuesCount.columns = ['release_date','counts']
		dfValuesCount.set_index('release_date',inplace=True)
		dfValuesCount.sort_values(by=['release_date'],inplace=True)
        
		# fill empty dates for regression
		startdate = f"{dfCopy['year'].min()}-01-01'"
		new_date_range = pd.date_range(start=startdate, end="2022-05-01", freq="D")
		dfValuesCount = dfValuesCount.reindex(new_date_range, fill_value=0)

		dfValuesCount['cumsum'] = dfValuesCount['counts'].cumsum()

		# selected dates for testing
		startMeasure = '2016-01-01'
		coronaDate = '2020-01-01'

		# create seperate dataframes based on before and after corona
		dfBeforeCovid = dfValuesCount[startMeasure:coronaDate]
		dfAfterCovid = dfValuesCount[coronaDate:]
		dfShort = dfValuesCount[startMeasure:]

		# https://ishan-mehta17.medium.com/simple-linear-regression-fit-and-prediction-on-time-series-data-with-visualization-in-python-41a77baf104c
		x = np.arange(dfBeforeCovid.index.size)
		print(x)
		fit = np.polyfit(x, dfBeforeCovid['cumsum'], deg=1)

		#Fit function : y = mx + c [linear regression ]
		fit_function = np.poly1d(fit)

		#Linear regression plot
		plt.figure(figsize=(15,6))
		
		plt.plot(dfBeforeCovid.index, fit_function(x),label='regression')
		#Time series data plot
		plt.plot(dfShort.index, dfShort['cumsum'],label='total')
		plt.axvline(pd.to_datetime(coronaDate), color="black",label='Start Corona')
		plt.legend()
		plt.grid()
		plt.ylim(ymin=0)
		plt.xlabel('Release Date')
		plt.ylabel('Total Games')
		plt.title(f'{genre} Regression')
		plt.savefig(f'./plots/regression/{genre}_regression.png')
		# plt.clf()

		prediction = fit_function(dfBeforeCovid.index.size + 100)
		print(f'prediction: {prediction}')

# ------------------------------------------------------------------------------
# Stats for genre

		dfCopy.set_index('release_date',inplace=True)
		dfCopy.sort_index()
		# https://stackoverflow.com/questions/48739374/pandas-plot-cumulative-sum-of-counters-over-time
		# total amount of games released
		dfCopy['total'] = 1
		dfCopy['cumsum'] = dfCopy['total'].cumsum()
		# Mean scores of the game
		dfCopy['pos_neg'] = dfCopy['positive'].astype(str)+"\t"+dfCopy['negative'].astype(str)
		dfCopy['score_rank'] = dfCopy['pos_neg'].map(lambda x:calculate_score(x.split('\t')[0],x.split('\t')[1]))
		# 5% of data used as rolling window
		rollingMeanValue = int(len(dfCopy)/20)
		dfCopy['score_mean'] = dfCopy['score_rank'].expanding(10).mean()
		dfCopy['score_rolling'] = dfCopy['score_rank'].rolling(rollingMeanValue).mean()
		# Mean price of the game
		dfCopy['price'] = dfCopy['price']/10 
		dfCopy['price_mean'] = dfCopy['price'].expanding(10).mean()
		# dfCopy['price_rolling'] = dfCopy['price'].rolling(rollingMeanValue).mean()

		maxRoundUp = roundup(dfCopy['price_mean'].max())

		# plot
		fig,ax = plt.subplots(figsize=(15, 6))
		fig.subplots_adjust(right=0.75)

		# for creating multiple y axis
		twin1 = ax.twinx()
		twin2= ax.twinx()

		twin2.spines.right.set_position(("axes", 1.2))

		labels = ['Total Games',
		'Mean Score',
		'Rolling Mean Score',
		'Mean Price',
		'Rolling Mean Price',
		'Start Corona']

		# total games line
		ln1 = ax.plot(dfCopy['cumsum'],color=color1,label=labels[0])
		ax.set_xlabel('Release Date')
		ax.set_ylabel(labels[0],color=color1)

		# mean score and price lines
		ln2 = twin1.plot(dfCopy['score_mean'],color=color2,label=labels[1])
		ln3 = twin1.plot(dfCopy['score_rolling'],color="darkred",label=labels[2])
		ln4 = twin2.plot(dfCopy['price_mean'],color=color3,label=labels[3])
		# ln5 = twin2.plot(dfCopy['price_rolling'],color="darkgreen",label=labels[4])

		lns = ln1+ln2+ln3+ln4

		# Coronadate line
		ln6 = ax.axvline(pd.to_datetime(coronaDate), color="black",label=labels[5])
		lns.append(ln6)

		ax.legend(handles=lns,loc=3)
		ax.grid()
		twin1.set_ylim(0,100)
		twin1.set_ylabel(f'{labels[1]} (%)', color=color2)
		twin2.set_ylim(0,maxRoundUp)
		twin2.set_ylabel(f'{labels[3]} (\N{euro sign})', color=color3)

		plt.title(f'{genre}')
		plt.savefig(f'./plots/{genre}_stats.png')
		plt.close()
		done = time.time()

		print(f"Total time: \t {done - start}")
		print("===========================")

total = time.time()
print(f"Total time: \t {total - initTime}")