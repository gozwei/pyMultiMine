import json
import os.path
import sys

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

for Coin in Config['coins']:
	print(Coin)
	print(Config['coins'][Coin])