import pandas as pd
import time
import matplotlib.pyplot as plt

initTime = time.time()

df = pd.read_csv("./data/0_Boxing_full.csv",encoding='utf-8-sig')

# change dateformat
df['release_date'] = pd.to_datetime(df['release_date'])
df = df.sort_values(by="release_date")

# https://stackoverflow.com/questions/48739374/pandas-plot-cumulative-sum-of-counters-over-time
dfAmount = df[['release_date']].copy()
dfAmount['total'] = 1
dfAmount.set_index('release_date',inplace=True)
dfAmount.sort_index().cumsum().plot()

# plot
plt.axvline('2019-07-24', color='red')
plt.xlabel('Release Date')
plt.ylabel('Total')
plt.title('Boxing')
plt.savefig('./plots/plot.png')


total = time.time()
print(f"Total time: \t {total - initTime}")
