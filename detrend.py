from pandas import read_csv
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot
import numpy
import pandas as pd

series = read_csv('./data/0_Pinball_full.csv',encoding='utf-8-sig')
# fit linear model
series2 = series[['release_date']].copy()
series2['release_date'] = pd.to_datetime(series2['release_date'])
series2 = series2.sort_values(by="release_date")
series2.set_index('release_date',inplace=True)
series2['total'] = 1
series2['cumsum'] = series2['total'].sort_index().cumsum()
del series2['total']
print(series2.head())

X = [i for i in range(0, len(series2))]
print(X)
X = numpy.reshape(X, (len(X), 1))
y = series2['cumsum'].values
print('----------------------')
print(y)
model = LinearRegression()
model.fit(X, y)
# calculate trend
trend = model.predict(X)
# plot trend
# pyplot.plot(y)
pyplot.plot(trend)
pyplot.show()

pyplot.title(f'trend')
pyplot.savefig(f'trend.png')
# detrend
detrended = [y[i]-trend[i] for i in range(0, len(series))]
# plot detrended
pyplot.clf()
pyplot.plot(detrended)

pyplot.title(f'detrend')
pyplot.savefig(f'detrend.png')
