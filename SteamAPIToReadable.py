import requests
import json
import pandas as pd
import os
from os.path import exists
import time

# dictionary with included genres with atleast 100 entries
# sorted from lowest amount to highest amount based on https://steamdb.info/tags/
genresDict = [
    "Basketball", "Spaceships", "Social Deduction", "Based On A Novel",
    "Farming", "Ambient", "Electronic Music", "Silent Protagonist", "Unforgiving",
    "Pinball", "Jet", "Outbreak Sim", "Golf", "Spelling", "Rome", "360 Video",
    "Epic", "Werewolves", "World War I", "Transhumanism", "Escape Room",
    "Boxing", "Horses", "Sniper", "Chess", "Mars", "Villain Protagonist",
    "Documentary", "Offroad", "Gambling", "Sailing", "Trivia", "Snow",
    "Soccer","Music-Based Procedural Generation", "Immersive", "Archery",
    "Time Attack", "Heist", "Diplomacy","On-Rails Shooter", "Party",
    "GameMaker", "Naval Combat", "Typing", "Transportation","Action RTS",
    "Illuminati", "Minigames", "Assassin", "Cold War","Party Game","Faith",
    "Cooking", "Dungeons & Dragons", "Vampire", "Superhero", "Auto Battler",
    "Real-Time with Pause", "Quick-Time Events", "Fishing", "Politics",
    "Dynamic Narration", "Dinosaurs", "Programming", "Western", "Naval",
    "Photo Editing", "Trading Card Game", "Underwater", "Dog", "Otome",
    "MOBA", "Mining", "Trains", "Hacking", "Underground", "Sokoban",
    "Martial Arts", "Hunting", "Time Travel", "FMV", "Trading", "Ninja",
    "Hex Grid", "Conspiracy", "Gothic", "Satire", "Tanks","Spectacle fighter",
    "Pirates","Political", "Combat Racing", "Creature Collector",
    "Real-Time", "Addictive", "Time Manipulation", "Agriculture",
    "Episodic", "Bullet Time", "Mechs", "Blood",
	"Automation", "Gun Customization", "Parody", "Capitalism", "Word Game",
	"Steampunk", "Software Training", "Farming Sim", "3D Vision", "America",
	"Solitaire", "Vehicular Combat", "Class-Based", "Mouse only", "Voxel",
	"Mystery Dungeon", "Colony Sim", "Open World Survival Craft",
	"Video Production","Dragons", "eSports", "Battle Royale", "Noir",
	"3D Fighter", "Swordplay", "Lovecraftian", "MMORPG", "Science",
	"Philosophical", "Card Battler", "Audio Production", "Cats",
	"Deckbuilding", "Dark Comedy", "Game Development", "Space Sim",
	"Mythology", "World War II", "Idler", "Rhythm", "Crime",
	"Collectathon", "Grid-Based Movement", "Parkour", "Twin Stick Shooter",
	"Animation & Modeling", "Supernatural", "Souls-like","Loot", "Beautiful",
	"Alternate History", "Hero Shooter", "Destruction",  "2D Fighter",
	"Comic Book", "Level Editor", "Dystopian", "Artificial Intelligence",
	"Runner", "Modern", "Lore-Rich", "Psychedelic", "Competitive",
	"Wargame", "Psychological", "Tactical RPG", "Thriller", "Nonlinear",
	"Beat 'em up", "Demons", "Fighting", "Team-Based", "Metroidvania",
	"Arena Shooter", "Perma Death", "Real Time Tactics", "4 Player Local",
	"City Builder", "Conversation", "Time Management", "Dark Humor",
	"Tower Defense", "Detective", "Flight", "Cinematic", "Aliens",
	"Economy", "Soundtrack", "Movie", "Clicker", "Robots", "LGBTQ+",
	"Board Game", "Classic", "Cyberpunk", "RPGMaker","Memes", "2.5D",
	"Third-Person Shooter", "Card Game", "Military", "Text-Based",
	"Web Publishing", "Action Roguelike", "RTS", "Fast-Paced", "Short",
	"Nature", "Isometric", "Score Attack","Stealth", "Top-Down Shooter",
	"Surreal", "Emotional", "Base Building", "Utilities", "Software",
	"Post-apocalyptic", "Bullet Hell", "Dungeon Crawler", "Zombies", 
	"War", "Resource Management", "Dark Fantasy", "Historical", 
	"Hack and Slash", "Interactive Fiction", "Turn-Based Tactics", 
	"Choose Your Own Adventure",  "Survival Horror", "JRPG", "Hidden Object", 
	"Education", "Cartoon", "Turn-Based Combat", "3D Platformer", 
	"Crafting", "Party-Based RPG", "Procedural Generation", 
	"Design & Illustration", "Turn-Based Strategy", "Logic", "Rogue-like", 
	"Futuristic", "Tabletop", "PvE", "Puzzle-Platformer", "Magic",
	"Hand-drawn", "Action RPG", "Management", "Building", "Side Scroller",
	"Character Customization", "Linear", "Medieval", "Space",
	"Multiple Endings", "Minimalist", "Point & Click", "Dark", "Mystery",
	"Sandbox", "Cartoony", "Physics", "Shoot 'Em Up", "2D Platformer",
	"PvP", "Choices Matter", "Racing", "Realistic","Top-Down", "FPS",
	"Comedy", "Co-op", "Survival", "Visual Novel", "Sports", "Difficult",
	"Third Person", "Open World", "Gore", "VR", "Female Protagonist",
	"Horror", "Retro", "Relaxing", "Platformer", "Violent",
	"Sci-fi", "Shooter", "Funny", "Arcade", "Anime", "First-Person",
	"Cute", "Exploration", "Multiplayer", "Funny", "Colorful", "Free to Play",
	"Fantasy", "Story Rich", "Pixel Graphics", "3D", "Atmospheric",
	"2D", "RPG", "Strategy", "Simulation", "Singleplayer", "Adventure",
	"Casual", "Action", "Indie"
]


def main():
	dataFolder = "./data/initial/"

	bulkNumber = 0 # start from which bulk(real time.csv)
	amountCounter = 0 # tracker for the amount of items in a bulk

	for i in genresDict:
		filename = 	dataFolder + str(bulkNumber) + "_" +  i + ".csv"
		# don"t make file again if already exist
		if(not os.path.exists(filename)):
			time.sleep(2)
			# response = requests.get(genresDict[i]).json()
			link = "https://steamspy.com/api.php?request=tag&tag=" + i
			response = requests.get(link).json()

			# Write output to a file
			# with open("output.json", "w") as json_file:
				# json_file.write(json.dumps(response, sort_keys=True, indent = 4))

			# read from file
			# df_json = pd.read_json("output.json")
			
			# convert json to csv
			df_json = pd.DataFrame.from_dict(response)
			# flip rows and columns
			df_json = df_json.transpose()
			
			df_json.to_csv(filename)

			print(f"Done with {filename}")
		# count the amount of items in the file for creating bulks of 2 hours
		with open(filename, "r") as fp:
			x = len(fp.readlines())
			amountCounter += x
			if(amountCounter > 3600):
				print(f"Total entries {amountCounter} for bulk {bulkNumber}" ) # 8
				amountCounter = 0
				bulkNumber += 1

	print(f"Length of genresDict: {len(genresDict)} ")

	printStat = False
	if(printStat):
		# print statistics for each file
		directory = os.fsencode(dataFolder)
		for file in os.listdir(directory):
			fileName = os.fsdecode(file)
			if fileName.endswith(".csv"):
				df = pd.read_csv(dataFolder + fileName)
				df = df[["appid","average_forever","negative","positive","name"]]
				print(f"--------------------------")
				print(f"Stats for {fileName}")
				print(f"--------------------------")
				print(df[["average_forever","negative","positive"]].describe())
				print(f"Highest average_forever \n {df[df.average_forever == df.average_forever.max()]}")
				print(f"Highest negative \n {df[df.negative == df.negative.max()]}")
				print(f"Highest positive \n {df[df.positive == df.positive.max()]}")


if __name__ == "__main__":
	main()