from pydoc import describe
import requests
import json
import pandas as pd
import os

# dictionary counting inlcluded genres
genresDict = {
'openWorld' : 'http://steamspy.com/api.php?request=tag&tag=Open+World',
'earlyAcces' : 'http://steamspy.com/api.php?request=tag&tag=Early+Access',
'racing' : 'http://steamspy.com/api.php?request=tag&tag=Racing',
'action' :'http://steamspy.com/api.php?request=tag&tag=Action'}


def main():
	makeData = False
	dataFolder = './data/'

	if makeData:
		for i in genresDict:
			response = requests.get(genresDict[i]).json()

			# creat temporary json file for pandas
			with open('tmp.json', 'w') as json_file:
				json_file.write(json.dumps(response, sort_keys=True, indent = 4))

			# convert json to csv
			df_json = pd.read_json('tmp.json')
			# flip rows and columns
			df_json = df_json.transpose()
			
			filename = 	'./data/' + i + '.csv'
			df_json.to_csv(filename)

		# remove temporary file
		os.remove('tmp.json')

	# print statistics for each file
	directory = os.fsencode(dataFolder)
	for file in os.listdir(directory):
		fileName = os.fsdecode(file)
		if fileName.endswith('.csv'):
			df = pd.read_csv(dataFolder + fileName)
			print('--------------------------')
			print('Stats for ' + fileName)
			print('--------------------------')
			print(df[['average_forever','negative','positive']].describe())
			print(f"Highest average_forever \n {df[df.average_forever == df.average_forever.max()]}")
			print(f"Highest negative \n {df[df.negative == df.negative.max()]}")
			print(f"Highest positive \n {df[df.positive == df.positive.max()]}")

if __name__ == '__main__':
	main()