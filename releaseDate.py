import requests
import pandas as pd
import time
import os
from os.path import exists
import numpy as np

def main():
	# the initial dataframe
	initDF = pd.DataFrame({ 'succes': [], 
							'coming_soon':[] , 
							'release_date':[],
							'steam_appid': []})

	initTime = time.time()
	bulkNumber = '91_'

	wait_time = []

	dataFolder = './data/initial/'
	directory = os.fsencode(dataFolder)
	# loop through all datasets
	for file in os.listdir(directory):	
		start = time.time()
		
		fileName = os.fsdecode(file)
		saveLocation = './data/' + fileName[:-4] + '_full.csv'

		if (fileName.startswith(bulkNumber) and fileName.endswith('.csv') and not os.path.exists(str(saveLocation))):
			dfGenres = pd.read_csv(dataFolder + fileName,encoding='utf-8-sig')

			print(f"Start with: \t {fileName}")
			# get every appid from dataset and call steam API
			appidsList = dfGenres['appid'].tolist()
			for i, appid in enumerate(appidsList,start=1):
				# limit of 200 request every 5min for API (1 call per 1.5s)
				starting = time.time()
				time.sleep(1.25)
				responseLink = 'https://store.steampowered.com/api/appdetails?appids='+ str(appid) + '&filters=release_date'
				try:
					response = requests.get(responseLink).json()
					# normalize the json
					dfReleaseDates = pd.json_normalize(response)
				except requests.exceptions.TooManyRedirects:
					# Tell the user their URL was bad and try a different one
					print(f"link not correcct: {responseLink}")
					continue
				except requests.exceptions.RequestException:  
					print(f"Failed appid:{appid}, \t url:  {responseLink}")
					continue

				# skip if fail (succes = false)
				if(len(dfReleaseDates.columns) != 3):	
					continue

				dfReleaseDates.columns = ['succes', 'coming_soon', 'release_date']

				# add the appid for merging
				dfReleaseDates['steam_appid'] = appid
				initDF = pd.concat((initDF,dfReleaseDates),axis=0)
				
				ending = time.time()
				wait_time.append(ending - starting)
				
				if(i % 500 == 0):
					done = time.time()
					print(f"Completed {i} entries")
					print(f"Mean loop time: \t {np.mean(wait_time)}")
					print(f"Total time: \t {done - start}")
					print("===========================")
					saveDateLocation = './data/dates/' + fileName[:-4] + '_dates_partial.csv'
					initDF.to_csv(saveDateLocation)

			
			# safe dates to a file
			saveDateLocation = './data/dates/' + fileName[:-4] + '_dates.csv'
			initDF.to_csv(saveDateLocation)
			# safe merged to a file
			merge = dfGenres.merge(initDF, left_on='appid', right_on='steam_appid')
			merge.to_csv(saveLocation)

			done = time.time()

			print(f"Done with: \t {fileName}")
			print(f"Mean loop time: \t {np.mean(wait_time)}")
			print(f"Total time: \t {done - start}")
			print("===========================")

	total = time.time()
	print(f"Total time: \t {total - initTime}")

if __name__ == '__main__':
	main()
