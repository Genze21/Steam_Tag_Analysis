from pandas import read_csv
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot
import numpy as np
import pandas as pd
import seaborn as sns

series = read_csv('./data/0_Pinball_full.csv',encoding='utf-8-sig')
# fit linear model
series2 = series[['release_date']].copy()
series2['release_date'] = pd.to_datetime(series2['release_date'])
series2 = series2.sort_values(by="release_date")
# data=series2.loc[series2['release_date']<'2020-01-01']
series2.set_index('release_date',inplace=True)
series2.index = series2.index.map(pd.Timestamp.toordinal)
series2['total'] = 1
series2['cumsum'] = series2['total'].sort_index().cumsum()
del series2['total']


# TODO
# https://stackoverflow.com/a/69171277

# convert the regression line start date to ordinal
x1 = pd.to_datetime('2019-01-02').toordinal()

# data slice for the regression line
data=series2.loc[:x1].reset_index()
print(data.head())

ax1 = data.plot(y='cumsum', c='k', figsize=(15, 6), grid=True, legend=False,
              title='Adjusted Close with Regression Line from 2019-01-02')

sns.regplot(data=data, x='release_date', y='cumsum', ax=ax1, color='magenta', scatter_kws={'s': 7}, label='Linear Model', scatter=False)

ax1.set_xlim(series2.index[0], series2.index[-1])

ax1.plot(series2['cumsum'])

# convert the axis back to datetime
xticks = ax1.get_xticks()
labels = [pd.Timestamp.fromordinal(int(label)).date() for label in xticks]
ax1.set_xticks(xticks)
ax1.set_xticklabels(labels)


ax1.legend()

pyplot.savefig(f'genre.png')

