from fileinput import filename
import requests
import json
import pandas as pd
import os
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

	bulkNumber = 0

	dataFolder = './data/initial/'
	directory = os.fsencode(dataFolder)
	# loop through all datasets
	for file in os.listdir(directory):	
		fileName = os.fsdecode(file)
		if  fileName.startswith(str(bulkNumber)) and fileName.endswith('.csv'):
			print(f"filename: {fileName}")
			dfGenres = pd.read_csv(dataFolder + fileName)

			# get every appid from dataset and call steam API
			appidsList = dfGenres['appid'].tolist()
			for appid in appidsList:
				responseLink = 'https://store.steampowered.com/api/appdetails?appids='+ str(appid) + '&filters=release_date'
				response = requests.get(responseLink).json()

				# normalize the json
				dfReleaseDates = pd.json_normalize(response)
				dfReleaseDates.columns = ['succes', 'coming_soon', 'release_date']

				# add the appid for merging
				dfReleaseDates['steam_appid'] = appid
				frames = [initDF, dfReleaseDates]
				initDF = pd.concat(frames)

				# limit of 200 request every 5min for API (1 call per 1.5s)
				time.sleep(2)
			
			# safe dates to a file
			saveLocation = './data/dates/' + fileName[:-4] + '_dates.csv'
			initDF.to_csv(saveLocation)
			# safe merged to a file
			saveLocation = './data/' + fileName[:-4] + '_full.csv'
			merge = dfGenres.merge(initDF, left_on='appid', right_on='steam_appid')
			merge.to_csv(saveLocation)
if __name__ == '__main__':
	main()