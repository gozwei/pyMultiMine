import json
import os.path
import sys
from time import sleep
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

MM = MultiMine()
if Config['config']['DryRun'] == 1:
	MM.SetDryRun()

MM.SetDebugTarget(Config['config']['DebugTarget'])

for CoinName in Config['coins']:
	if Config['coins'][CoinName]["Enabled"]:
		C = Coin(CoinName, Config['coins'][CoinName]["FullName"])
		C.SetHashRate(Config['coins'][CoinName]["HashRate"])
		C.SetExecutable(Config['coins'][CoinName]["Executable"])
		if Config['coins'][CoinName]["Default"]:
			C.SetAsDefault()
		C.SetMinimumMineTime(Config['coins'][CoinName]["MinMineTime"])
		MM.AddCoin(C)

while True:
	MM.GetBTCUSD()
	MM.GetCoinStats()
	MM.MineMostProfitable()
	sleep(Config['config']['CheckCoinsEvery'])
