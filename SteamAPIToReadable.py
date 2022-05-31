import requests
import json
import pandas as pd
import os

# dictionary with included genres
genresDict = {
'2D Platformer' : 'http://steamspy.com/api.php?request=tag&tag=2D+Platformer',	
'action' 		: 'http://steamspy.com/api.php?request=tag&tag=Action',
'earlyAcces' 	: 'http://steamspy.com/api.php?request=tag&tag=Early+Access',
'openWorld' 	: 'http://steamspy.com/api.php?request=tag&tag=Open+World',
'racing' 		: 'http://steamspy.com/api.php?request=tag&tag=Racing',
'sandbox' 		: 'http://steamspy.com/api.php?request=tag&tag=Sandbox',
'tactical' 		: 'http://steamspy.com/api.php?request=tag&tag=Tactical',
}


def main():
	makeData = False
	dataFolder = './data/'

	if makeData:
		for i in genresDict:
			response = requests.get(genresDict[i]).json()

			# Write output to a file
			# with open('output.json', 'w') as json_file:
				# json_file.write(json.dumps(response, sort_keys=True, indent = 4))

			# read from file
			# df_json = pd.read_json('output.json')
			
			# convert json to csv
			df_json = pd.DataFrame.from_dict(response)
			# flip rows and columns
			df_json = df_json.transpose()
			
			filename = 	'./data/' + i + '.csv'
			df_json.to_csv(filename)

	# print statistics for each file
	directory = os.fsencode(dataFolder)
	for file in os.listdir(directory):
		fileName = os.fsdecode(file)
		if fileName.endswith('.csv'):
			df = pd.read_csv(dataFolder + fileName)
			df = df[['appid','average_forever','negative','positive','name']]
			print(f"--------------------------")
			print(f"Stats for {fileName}")
			print(f"--------------------------")
			print(df[['average_forever','negative','positive']].describe())
			print(f"Highest average_forever \n {df[df.average_forever == df.average_forever.max()]}")
			print(f"Highest negative \n {df[df.negative == df.negative.max()]}")
			print(f"Highest positive \n {df[df.positive == df.positive.max()]}")


if __name__ == '__main__':
	main()