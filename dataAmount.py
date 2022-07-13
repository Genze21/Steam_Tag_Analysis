import os

def main():
	dataFolder = './data/'
	directory = os.fsencode(dataFolder)
	# loop through all datasets
	total = 0

	tooShort = []

	for file in os.listdir(directory):	
		fileName = os.fsdecode(file)

		if (fileName.endswith('.csv')):
			# test if data is too small
			with open("./data/" + fileName, "r") as fp:
				x = len(fp.readlines())
				minAmount = 100

				if(x < minAmount):
					print(f"Total entries {x}, for file: {fileName} has less than {minAmount} \t ")
					tooShort.append(fileName)
					total += 1

	print(f"Total with too low amount {total}" ) # 8
	return(tooShort)

if __name__ == '__main__':
	main()