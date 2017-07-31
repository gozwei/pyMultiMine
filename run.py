import json
import os.path
import sys
from MultiMine import MultiMine
from MultiMineCoin import Coin

if len(sys.argv) < 2:
	print("No config specified!")
	exit()

ConfigFile = sys.argv[1]

if not os.path.isfile(ConfigFile):
	print("File", ConfigFile, "does not exist!")
	exit()

with open(ConfigFile) as ConfigFileHandle:    
    Config = json.load(ConfigFileHandle)

print(Config)
print()

MM = MultiMine()

for CoinName in Config['coins']:
	print(CoinName, Config['coins'][CoinName]["FullName"])
	C = Coin(CoinName, Config['coins'][CoinName]["FullName"])

	# print(Config['coins'][Coin])