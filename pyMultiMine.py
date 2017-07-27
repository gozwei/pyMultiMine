import json
import urllib.request
from time import sleep
import shlex, subprocess
import time
import datetime

def datestr(type="std"):
	ts = time.time()
	if type == "file":
		return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S') + ".log"
	else:
		return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

LogFileName = datestr(type="file")

class MultiMine():
	def __init__(self):
		print('Multi Miner initiated')
		self.coins = []

		self.rates = dict()
		self.rates["Equihash"] = 3.4e3
		self.rates["Myriad-Groestl"] = 520e6
		self.rates["LBRY"] = 2323e6

	def AddCoin(self, coin):
		self.coins.append(coin)

	def GetCoinStats(self):
		hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		   'Accept-Encoding': 'none',
		   'Accept-Language': 'en-US,en;q=0.8',
		   'Connection': 'keep-alive'}

		response = urllib.request.Request('https://www.whattomine.com/coins.json#',headers=hdr)
		response = urllib.request.urlopen(response)
		html = response.read()
		json1_data = json.loads(str(html.decode('UTF-8')))
		for myCoin in self.coins:
			# print('Looking for ', myCoin.Name)
			for coin in json1_data["coins"].items():
				CoinInfo = coin[1]
				CoinName = coin[0]
				# print(CoinName, CoinName == myCoin.FullName)
				if CoinName == myCoin.FullName:
					Difficulty = CoinInfo["difficulty"] 
					BlockTime = float(CoinInfo["block_time"])
					NetHashRate =float(CoinInfo["nethash"])
					BlockSize = CoinInfo["block_reward"] 
					Price = CoinInfo["exchange_rate"] 
					myCoin.SetMiningParameters(Difficulty, BlockTime, NetHashRate, BlockSize, Price)
					myCoin.SetHashRate(self.rates[CoinInfo["algorithm"]])
					myCoin.CalcProfit()
					with open(LogFileName, "a") as myfile:
						myfile.write("{0:s}\tprofit\t{1:s}\t{2:8.6f}\n".format(datestr(), myCoin.Name, myCoin.Profit))

		self.coins.sort(key=lambda x: x.Profit, reverse=True)

	def Print(self):

		for myCoin in self.coins:
			myCoin.Print()

	def MineMostProfitable(self):
		CoinToMine = self.coins[0]
		print("\tAttempt to start mining ", CoinToMine.FullName)
		if CoinToMine.ActiveMining:
			print("\t", CoinToMine.FullName, " is allraedy mining")
			with open(LogFileName, "a") as myfile:
				myfile.write("{0:s}\tcontinue\t{1:s}\t{2:8.6f}\n".format(datestr(), CoinToMine.Name, CoinToMine.Profit))
		else:
			for myCoin in self.coins:
				if myCoin.ActiveMining:
					myCoin.StopMining()
					print("\tAttempt to stop mining ", myCoin.FullName)
			CoinToMine.StartMining()
			print("\tStart mining ", CoinToMine.FullName)
			print()


class Coin():
	def __init__(self, Name, FullName):
		self.Name = Name
		self.FullName = FullName
		self.Profit = 0
		self.ActiveMining = False

	def SetExecutable(self, executable):
		self.executable = executable

	def StartMining(self):
		if self.ActiveMining == False:
			self.ActiveMining = True
			args = shlex.split(self.executable)
			self.process = subprocess.Popen(args)
			with open(LogFileName, "a") as myfile:
				myfile.write("{0:s}\tstart\t{1:s}\t{2:8.6f}\n".format(datestr(), self.Name, self.Profit))

	def StopMining(self):
		if self.ActiveMining == True:
			self.process.terminate()
			self.ActiveMining = False
			with open(LogFileName, "a") as myfile:
				myfile.write("{0:s}\tstop\t{1:s}\n".format(datestr(), self.Name))

	def SetMiningParameters(self, Difficulty, BlockTime, NetHashRate, BlockSize, Price):
		self.Difficulty = Difficulty
		self.BlockTime = BlockTime
		self.NetHashRate = NetHashRate
		self.BlockSize = BlockSize
		self.Price = Price

	def SetHashRate(self, HashRate):
		self.HashRate = HashRate

	def CalcProfit(self):
		A = self.Difficulty / self.BlockTime
		B = self.HashRate / self.NetHashRate
		C = (60 / self.BlockTime) * self.BlockSize
		D = B * C
		E = D * 1440 * self.Price 
		self.Profit = E

	def Print(self):
		print(self.Name, self.Profit)


MM = MultiMine()

ZEC = Coin("ZEC", "Zcash")
ZEC.SetExecutable("/home/goto/Documents/0.3.4b/miner --server eu1-zcash.flypool.org --user t1bXpK7mgBJo5hP1rSCU4s6cwekX6gXHG9x.rig1 --pass x --port 3333 --pec --fee 0 --api 10.22.3.84:42555")
MM.AddCoin(ZEC)

LBRY = Coin("LBRY", "LBRY")
LBRY.SetExecutable("/home/goto/ccminer/ccminer -a lbry -o stratum+tcp://lbry.suprnova.cc:6256 -u gozwei.rig1 -p x")
MM.AddCoin(LBRY)

DGB = Coin("DGB", "DGB-Groestl")
DGB.SetExecutable("/home/goto/ccminer/ccminer -a myr-gr -o stratum+tcp://dgbg.suprnova.cc:7978 -u gozwei.rig1 -p x")
MM.AddCoin(DGB)


while True:
	MM.GetCoinStats()
	MM.MineMostProfitable()
	sleep(60)


MM.Print()
