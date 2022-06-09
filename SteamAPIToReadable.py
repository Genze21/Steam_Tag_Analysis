import requests
import json
import pandas as pd
import os
from os.path import exists

# dictionary with included genres with atleast 100 entries
# sorted from lowest amount to highest amount based on https://steamdb.info/tags/
genresDict = [
    'Basketball', 'Spaceships', 'Social Deduction', 'Based On A Novel',
    'Farming', 'Ambient', 'Electronic Music', 'Silent Protagonist', 'Unforgiving',
    'Pinball', 'Jet', 'Outbreak Sim', 'Golf', 'Spelling', 'Rome', '360 Video',
    'Epic', 'Werewolves', 'World War I', 'Transhumanism', 'Escape Room',
    'Boxing', 'Horses', 'Sniper', 'Chess', 'Mars', 'Villain Protagonist',
    'Documentary', 'Offroad', 'Gambling', 'Sailing', 'Trivia', 'Snow',
    'Soccer','Music-Based Procedural Generation', 'Immersive', 'Archery',
    'Time Attack', 'Heist', 'Diplomacy','On-Rails Shooter', 'Party',
    'GameMaker', 'Naval Combat', 'Typing', 'Transportation','Action RTS',
    'Illuminati', 'Minigames', 'Assassin', 'Cold War','Party Game','Faith',
    'Cooking', 'Dungeons & Dragons', 'Vampire', 'Superhero', 'Auto Battler',
    'Real-Time with Pause', 'Quick-Time Events', 'Fishing', 'Politics',
    'Dynamic Narration', 'Dinosaurs', 'Programming', 'Western', 'Naval',
    'Photo Editing', 'Trading Card Game', 'Underwater', 'Dog', 'Otome',
    'MOBA', 'Mining', 'Trains', 'Hacking', 'Underground', 'Sokoban',
    'Martial Arts', 'Hunting', 'Time Travel', 'FMV', 'Trading', 'Ninja',
    'Hex Grid', 'Conspiracy', 'Gothic', 'Satire', 'Tanks','Spectacle fighter',
    'Pirates','Political', 'Combat Racing', 'Creature Collector',
    'Real-Time', 'Addictive', 'Time Manipulation', 'Agriculture',
    'Episodic', 'Bullet Time'

    # 'action',
    # 'earlyAcces',
    # 'openWorld',
    # 'racing',
    # 'sandbox',
    # 'tactical',
    # 'steamMachine',
]


def main():
	dataFolder = './data/initial/'

	bulkNumber = 0 # start from which bulk(real time.csv)
	amountCounter = 0

	for i in genresDict:
		filename = 	dataFolder + str(bulkNumber) + '_' +  i + '.csv'
		# don't make file again if already exist
		if(not os.path.exists(filename)):
			# response = requests.get(genresDict[i]).json()
			link = "https://steamspy.com/api.php?request=tag&tag=" + i
			response = requests.get(link).json()

			# Write output to a file
			# with open('output.json', 'w') as json_file:
				# json_file.write(json.dumps(response, sort_keys=True, indent = 4))

			# read from file
			# df_json = pd.read_json('output.json')
			
			# convert json to csv
			df_json = pd.DataFrame.from_dict(response)
			# flip rows and columns
			df_json = df_json.transpose()
			
			df_json.to_csv(filename)

		# count the amount of items in the file
		print(f"Done with {filename}")
		with open(filename, 'r') as fp:
			x = len(fp.readlines())
			amountCounter += x
			if(amountCounter > 1800):
				print('Total entries', amountCounter) # 8
				amountCounter = 0
				bulkNumber += 1


	printStat = False
	if(printStat):
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