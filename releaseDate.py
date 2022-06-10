from fileinput import filename
import requests
import json
import pandas as pd
import os
from os.path import exists
import time

# response = requests.get(" https://store.steampowered.com/api/appdetails?appids=10&filters=release_date")
# response = requests.get(" https://store.steampowered.com/api/appdetails?appids=1000750&filters=price_overview,release_date")
# print(json.dumps(response.json(), sort_keys=True, indent = 4))

def main():
	# the initial dataframe
	initDF = pd.DataFrame({ 'succes': [], 
							'coming_soon':[] , 
							'release_date':[],
							'steam_appid': []})

	initTime = time.time()
	bulkNumber = '2_'

	dataFolder = './data/initial/'
	directory = os.fsencode(dataFolder)
	# loop through all datasets
	for file in os.listdir(directory):	
		start = time.time()
		
		fileName = os.fsdecode(file)
		saveLocation = './data/' + fileName[:-4] + '_full.csv'

		if (fileName.startswith(bulkNumber) and fileName.endswith('.csv') and not os.path.exists(str(saveLocation))):
			dfGenres = pd.read_csv(dataFolder + fileName)

			print(f"Start with: \t {fileName}")
			# get every appid from dataset and call steam API
			appidsList = dfGenres['appid'].tolist()
			for appid in appidsList:
				# limit of 200 request every 5min for API (1 call per 1.5s)
				time.sleep(2)
				
				responseLink = 'https://store.steampowered.com/api/appdetails?appids='+ str(appid) + '&filters=release_date'
				try:
					response = requests.get(responseLink).json()
					response.raise_for_status()
				except requests.exceptions.TooManyRedirects:
					# Tell the user their URL was bad and try a different one
					print(f"link not correcct: {responseLink}")
				except requests.exceptions.RequestException as e:  
					print(f"Failed appid:{appid}, \t url:  {responseLink}")
					print(e)
					raise SystemExit(e)
					continue
				# normalize the json
				dfReleaseDates = pd.json_normalize(response)

				# skip if fail (succes = false)
				if(len(dfReleaseDates.columns) != 3):	
					continue

				dfReleaseDates.columns = ['succes', 'coming_soon', 'release_date']

				# add the appid for merging
				dfReleaseDates['steam_appid'] = appid
				frames = [initDF, dfReleaseDates]
				initDF = pd.concat(frames)

			
			# safe dates to a file
			saveDateLocation = './data/dates/' + fileName[:-4] + '_dates.csv'
			initDF.to_csv(saveDateLocation)
			# safe merged to a file
			merge = dfGenres.merge(initDF, left_on='appid', right_on='steam_appid')
			merge.to_csv(saveLocation)

			done = time.time()

			print(f"Done with: \t {fileName}")
			print(f"Time: \t {done - start}")
			print("===========================")

	total = time.time()
	print(f"Total time: \t {total - initTime}")


if __name__ == '__main__':
	main()