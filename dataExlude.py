import os

def main():
	dataFolder = './data/'
	directory = os.fsencode(dataFolder)

	# List with exluded genres, start with overlapping genres
	exludeList = ['0_Outbreak Sim_full.csv', '1_Action RTS.csv',
				'6_Farming Sim_full.csv','9_Space Sim_full.csv', 
				'30_Survival Horror_full.csv', '38_Action RPG_full.csv',
				'7_Open World Survival Craft_full.csv','21_Third-Person Shooter_full.csv',
				]


	# loop through all datasets
	for file in os.listdir(directory):	
		fileName = os.fsdecode(file)

		if (fileName.endswith('.csv')):
			# test if data is too small
			with open("./data/" + fileName, "r") as fp:
				x = len(fp.readlines())
				minAmount = 100

				if(x < minAmount):
					print(f"Total entries {x}, for file: {fileName} has less than {minAmount} \t ")
					exludeList.append(fileName)


	print(f"Total with excluded {len(exludeList)}" ) # 8
	return(exludeList)

if __name__ == '__main__':
	main()