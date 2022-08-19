from statistics import mode
import pandas as pd
import time
import matplotlib.pyplot as plt
import math 
import os
import scipy.stats as stats
from scipy.stats import pearsonr,spearmanr
import dataAmount
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from statsmodels.stats.weightstats import ttest_ind

initTime = time.time()

# files that have less than 100 entires
tooShort = dataAmount.main()

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

slopeIncrease = []
slopeDecrease = []
slopeEven = []


statAnalysis = {}
genreList = []
statisticList = []
pvalueList = []

scoreIncrease = []
scoreDecrease = []
scoreEven = []

priceIncrease = []
priceDecrease = []
priceEven = []

# loop through all datasets
for file in os.listdir(directory):	
	start = time.time()

	fileName = os.fsdecode(file)

	if (fileName.endswith('.csv') and fileName not in tooShort):
	# if (fileName == '0_Pinball_full.csv'):
	# if (fileName == '8_Audio Production_full.csv'):
	# if (fileName == '88_Action_full.csv'):
	# if (fileName == '58_Female Protagonist_full.csv'):

	# if ((fileName == '0_Pinball_full.csv') or (fileName == '8_Audio Production_full.csv') 
	# or (fileName == '88_Action_full.csv') or (fileName == '58_Female Protagonist_full.csv')):

		print(f"Start with: \t {fileName}")

		df = pd.read_csv('./data/' + fileName,encoding='utf-8-sig')
		genre = fileName.split('_')[1]

		# seperate date into day, month and year
		df[["day", "month", "year"]] = df["release_date"].str.split(" ", expand = True)
		# change month to numerical value
		df['month'] = df['month'].map(lambda x:monthConvert(x))
		df['year'] = pd.to_numeric(df['year'])

		# convert dateformat
		df['release_date'] = pd.to_datetime(df['release_date'])
		df = df.sort_values(by="release_date")

		# create graph of total amount of games, mean score, mean price
		dfCopy = df[['release_date','score_rank','positive','negative','price','year','month','day']].copy()

# Regression for genre -------------------------------------------------------------------
		# convert value counts to a dataframe
		dfValuesCount = pd.DataFrame(dfCopy['release_date'].value_counts())
		dfValuesCount = dfValuesCount.reset_index()
		dfValuesCount.columns = ['release_date','counts']
		dfValuesCount.set_index('release_date',inplace=True)
		dfValuesCount.sort_values(by=['release_date'],inplace=True)
        
		# fill empty dates for regression
		startYear = int(dfCopy['year'].min())
		startdate = f"{startYear}-01-01'"
		new_date_range = pd.date_range(start=startdate, end="2022-05-01", freq="D")
		dfValuesCount = dfValuesCount.reindex(new_date_range, fill_value=0)

		dfValuesCount['cumsum'] = dfValuesCount['counts'].cumsum()

		# selected dates for testing
		startMeasure = '2017-01-01'
		coronaDate = '2020-01-01'

		# create seperate dataframes based on before and after corona
		dfShort = dfValuesCount[startMeasure:].copy()
		
		dfBeforeCovid = dfShort[startMeasure:coronaDate].copy()
		dfBeforeCovid['days_from_start'] = (dfBeforeCovid.index - dfBeforeCovid.index[0]).days; 

		dfAfterCovid = dfShort[coronaDate:].copy()
		dfAfterCovid['days_from_start'] = (dfAfterCovid.index - dfAfterCovid.index[0]).days; 

		dfBeforeCovidCopy = dfBeforeCovid.copy()
		dfBeforeCovidCopy = dfBeforeCovidCopy.drop('cumsum', axis=1)
		dfBeforeCovidCopy['cumsum'] = dfBeforeCovidCopy['counts'].cumsum()

		dfAfterCovidCopy = dfAfterCovid.copy()
		dfAfterCovidCopy = dfAfterCovidCopy.drop('cumsum', axis=1)
		dfAfterCovidCopy['cumsum'] = dfAfterCovidCopy['counts'].cumsum()

		# https://stackoverflow.com/questions/66110650/how-to-compare-the-slopes-of-two-regression-lines
		before_slope, before_coef = np.polyfit(dfBeforeCovidCopy['days_from_start'], dfBeforeCovidCopy['cumsum'], 1)
		after_slope, after_coef = np.polyfit(dfAfterCovidCopy['days_from_start'], dfAfterCovidCopy['cumsum'], 1)
		# print("-----")

		if((before_slope - after_slope) <= -0.02):
			slopeIncrease.append(genre)
		elif((before_slope - after_slope) >= 0.02):
			slopeDecrease.append(genre)
		else:
			slopeEven.append(genre)



		N = len(dfAfterCovidCopy)
		dftmp = dfBeforeCovidCopy[(dfBeforeCovidCopy['days_from_start'] < N) ]

		blue_y = dftmp['cumsum'].to_numpy()
		light_blue_y = dfAfterCovidCopy['cumsum'].to_numpy()

		y = blue_y-light_blue_y
		# Let create a linear regression
		mod = sm.OLS(y, sm.add_constant(dfAfterCovidCopy['days_from_start']))
		res = mod.fit()

		# print(res.summary())
		# print(res.summary2().tables[1]['P>|t|'])
		# print(res.pvalues)
		# https://ishan-mehta17.medium.com/simple-linear-regression-fit-and-prediction-on-time-series-data-with-visualization-in-python-41a77baf104c
		x = np.arange(dfBeforeCovid.index.size)
		fit = np.polyfit(x, dfBeforeCovid['cumsum'], deg=1)

		#Fit function : y = mx + c [linear regression ]
		fit_function = np.poly1d(fit)
		line1 = fit_function.c

		size = dfBeforeCovid.size

		def correlationValues(line,length):
			x = []
			for i in range(length):
				x.append((line[0]) * i + line[1])
				x.append((line[0]) * i)
			return(x)

		# print(f"reg before:{fit_function}")
		beforeValues = correlationValues(line1,size)

		x = dfBeforeCovid['days_from_start'].values.reshape(-1, 1)
		y = dfBeforeCovid['cumsum'].values

		model = LinearRegression().fit(x, y)
		r_sq = model.score(x, y)
		# print(f"coefficient of determination: {r_sq}")
		# print(f"intercept: {model.intercept_}")
		# print(f"slope: {model.coef_}")

		y_pred = model.predict(x)
		# print(f"predicted response:\n{y_pred}")

		# print(model.summary())

		mod = sm.OLS(y, x)
		fii = mod.fit()
		# print(fii.summary())
		p_values = fii.summary2().tables[1]['P>|t|']
		# print(p_values)


		plt.figure(figsize=(15,6))
		
		#Linear regression plot
		plt.plot(dfShort.index, dfShort['cumsum'],label='total', color=color1)
		reg1 = plt.plot(dfBeforeCovid.index, fit_function(x),label='regression before Covid',color=color2)
		
		x = np.arange(dfAfterCovid.index.size)
		fit = np.polyfit(x, dfAfterCovid['cumsum'], deg=1)

		#Fit function : y = mx + c [linear regression ]
		fit_function = np.poly1d(fit)
		line2 = fit_function.c
		b = [1,line2[0]]
		# print(f"reg after:{fit_function}")

		afterValues = correlationValues(line2,size)

		# https://www.geeksforgeeks.org/how-to-conduct-a-two-sample-t-test-in-python/
		# Conducting two-sample ttest

		# print(stats.ttest_ind(a=beforeValues, b=afterValues, equal_var=True))

		statValue,pvalue = stats.ttest_ind(a=beforeValues, b=afterValues, equal_var=True)
		
		genreList.append(genre)
		statisticList.append(statValue)
		pvalueList.append(pvalue)
		# print("-------")
		# result = pg.ttest(beforeValues, afterValues, correction=True)
		
		# Print the result
		# print(result)


		# print(ttest_ind(beforeValues, afterValues))


		corr = np.corrcoef(beforeValues,afterValues) 
		# print(corr)
		# print(corr[0][1])
		# print(corr[1][0])

		reg2 = plt.plot(dfAfterCovid.index, fit_function(x),label='regression after Covid', color=color3)
		#Time series data plot	
		
		plt.axvline(pd.to_datetime(coronaDate), color="black",label='Start Corona')
		
		plt.legend()
		plt.grid()
		plt.ylim(ymin=0)
		
		plt.xlabel('Release Date')
		plt.ylabel('Total Games')
		plt.title(f'{genre} Regression')
		plt.savefig(f'./plots/regression/{genre}_regression.png')
		# plt.clf()
		plt.close()
		# prediction output
		# prediction = fit_function(dfBeforeCovid.index.size + 100)
		# print(f'prediction: {prediction}')

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

		roundUpValue = roundup(dfCopy['price_mean'].max())
		labels = ['Total Games',
		'Mean Score',
		'Rolling Mean Score',
		'Mean Price',
		'Rolling Mean Price',
		'Start Corona']

		scoreBefore = dfCopy['score_mean'].loc[(dfCopy['year'] < 2020)].iloc[-1]
		scoreAfter = dfCopy['score_mean'].iloc[-1]
		if(scoreBefore - scoreAfter >= 5):
			scoreDecrease.append(genre)
		elif(scoreBefore - scoreAfter <= -5 ):
			scoreIncrease.append(genre)
		else:
			scoreEven.append(genre)

		priceBefore = dfCopy['price_mean'].loc[(dfCopy['year'] < 2020)].iloc[-1]
		priceAfter = dfCopy['price_mean'].iloc[-1]
		if(priceBefore - priceAfter >= 5):
			priceDecrease.append(genre)
		elif(priceBefore - priceAfter <= -5 ):
			priceIncrease.append(genre)
		else:
			priceEven.append(genre)

		# stats in seperate plots
		# plt.figure(figsize=(15, 6))
		# plt.plot(dfCopy['cumsum'],color=color1,label=labels[0])
		# plt.axvline(pd.to_datetime(coronaDate), color="black",label=labels[5])
		# plt.grid()
		# plt.legend()
		# plt.savefig(f'./plots/releases/{genre}_release.png')
		# plt.clf()

		# plt.grid()
		# plt.plot(dfCopy['score_mean'],color=color2,label=labels[1])
		# plt.plot(dfCopy['score_rolling'],color="darkred",label=labels[2])
		# plt.ylim(0,100)
		# plt.axvline(pd.to_datetime(coronaDate), color="black",label=labels[5])
		# plt.legend()
		# plt.title(f'{genre} Score')	
		# plt.savefig(f'./plots/score/{genre}_score.png')
		# plt.clf()

		# plt.grid()
		# plt.plot(dfCopy['price_mean'],color=color3,label=labels[3])
		# plt.title(f'{genre} Price')	
		# plt.ylim(0,roundUpValue)
		# plt.axvline(pd.to_datetime(coronaDate), color="black",label=labels[5])
		# plt.legend()
		# plt.savefig(f'./plots/price/{genre}_price.png')
		# plt.close()		

		# plot 
		fig,ax = plt.subplots(figsize=(15, 6))
		fig.subplots_adjust(right=0.75)


		# for creating multiple y axis
		twin1 = ax.twinx()
		twin2= ax.twinx()

		twin2.spines.right.set_position(("axes", 1.2))


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
		twin2.set_ylim(0,roundUpValue)
		twin2.set_ylabel(f'{labels[3]} (\N{euro sign})', color=color3)

		plt.title(f'{genre} Stats')	
		plt.savefig(f'./plots/{genre}_stats.png')
		plt.close()

# ------------------------------------------------------------------------------
# trend and detrend

		X = [i for i in range(0, len(dfCopy))]
		X = np.reshape(X, (len(X), 1))
		y = dfCopy['cumsum'].values
		model = LinearRegression()
		model.fit(X, y)
		# calculate trend
		trend = model.predict(X)
		# plot trend
		plt.clf()
		plt.plot(trend)

		plt.title(f'{genre} trend')	
		plt.savefig(f'./plots/trend/{genre}_trend.png')
		# detrend
		detrended = [y[i]-trend[i] for i in range(0, len(df))]
		# plot detrended
		plt.clf()
		plt.plot(detrended)

		plt.title(f'{genre} detrend')	
		plt.savefig(f'./plots/detrend/{genre}_detrend.png')

		done = time.time()

		print(f"Loop time: \t {done - start}")
		print("===========================")

total = time.time()
with open ('slopes.txt','w') as f:
	f.write((f"Total slope increase: \t {len(slopeIncrease)}"))
	f.write('\n')
	f.write((f"Total slope decrease: \t {len(slopeDecrease)}"))
	f.write('\n')
	f.write((f"Total slope even: \t {len(slopeEven)}"))

with open ('scores.txt','w') as f:
	f.write((f"Total score increase: \t {len(scoreIncrease)}"))
	f.write('\n')
	f.write((f"Total score decrease: \t {len(scoreDecrease)}"))
	f.write('\n')
	f.write((f"Total score even: \t {len(scoreEven)}"))

with open ('price.txt','w') as f:
	f.write((f"Total price increase: \t {len(priceIncrease)}"))
	f.write('\n')
	f.write((f"Total price decrease: \t {len(priceDecrease)}"))
	f.write('\n')
	f.write((f"Total price even: \t {len(priceEven)}"))

# with open ('t-test.csv','w') as f:
# 	f.write((f"genre, statistics ,pvalue"))
# 	f.write('\n')
# 	for count,value in enumerate (genreList):
# 		f.write((f"{genreList[count]}, {statisticList[count]} ,{pvalueList[count]}"))
# 		f.write('\n')

print(f"Total time: \t {total - initTime}")