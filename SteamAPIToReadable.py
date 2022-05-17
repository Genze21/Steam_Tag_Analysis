import requests
import json
import pandas as pd
import os

genresDict = {
'openWorld' : 'http://steamspy.com/api.php?request=tag&tag=Open+World',
'earlyAcces' : 'http://steamspy.com/api.php?request=tag&tag=Early+Access',
'racing' : 'http://steamspy.com/api.php?request=tag&tag=Racing',
'action' :'http://steamspy.com/api.php?request=tag&tag=Action'}


for i in genresDict:
	response = requests.get(genresDict[i]).json()

	# creat temporary json file for pandas
	with open('tmp.json', 'w') as json_file:
		json_file.write(json.dumps(response, sort_keys=True, indent = 4))

	# convert json to csv
	df_json = pd.read_json('tmp.json')
	# delete temporary file
	
	filename = 	'./data/' + i + '.csv'
	df_json.to_csv(filename)

# remove temporary file
os.remove('tmp.json')