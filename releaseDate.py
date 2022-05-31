import requests
import json
import pandas as pd
import os
import time

# response = requests.get(" https://store.steampowered.com/api/appdetails?appids=10&filters=release_date")
# response = requests.get(" https://store.steampowered.com/api/appdetails?appids=1000750&filters=price_overview,release_date")
# print(json.dumps(response.json(), sort_keys=True, indent = 4))

# dictionary with some appids
tempArr = {
	"1000750" : "https://store.steampowered.com/api/appdetails?appids=1000750&filters=release_date",
	"1003190" : "https://store.steampowered.com/api/appdetails?appids=1003190&filters=release_date"
}

def main():
	# the initial dataframe
	initDF = pd.DataFrame({ 'succes': [], 
							'coming_soon':[] , 
							'release_date':[],
							'steam_appid': []})
	# loop through all avaiable appid
	for i in tempArr:
		response = requests.get(tempArr[i]).json()

		# normalize the json
		df = pd.json_normalize(response)
		df.columns = ['succes', 'coming_soon', 'release_date']
		# add the appid for merging
		df['steam_appid'] = i
		frames = [initDF, df]
		initDF = pd.concat(frames)
		# print to terminal
		print(df)
		# limit of 200 request every 5min for API (1 call per 1.5s)
		time.sleep(2)

	initDF.to_csv('./data/output.csv')

if __name__ == '__main__':
	main()