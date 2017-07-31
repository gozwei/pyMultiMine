import json
import urllib.request
from time import sleep
import shlex, subprocess
import time
import datetime
from MultiMineCommon import Common

class MultiMine():
	def __init__(self):
		print('Multi Miner initiated')
		self.coins = []

		self.rates = dict()
		self.rates["Equihash"] = 3.4e3
		self.rates["Myriad-Groestl"] = 520e6
		self.rates["LBRY"] = 2323e6
		self.rates["NeoScrypt"] = 6600e3

	def AddCoin(self, coin):
		self.coins.append(coin)

	def GetCoinStats(self):
		html = GetURL("https://www.whattomine.com/coins.json")
		if html != "Error":
			json1_data = json.loads(html)
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
							myfile.write("{0:s}\tprofit\t{1:s}\t{2:8.6f}\t{3:8.6f}\n".format(datestr(), myCoin.Name, myCoin.Profit, myCoin.ProfitBTC))
		else:
			for myCoin in self.coins:
				if myCoin.Default:
					myCoin.Profit = 0
					myCoin.ProfitBTC = 0
					with open(LogFileName, "a") as myfile:
						myfile.write("{0:s}\terror fetching data, mining default\t{1:s}\n".format(datestr(), myCoin.Name))
				else:
					myCoin.Profit = -1
					myCoin.ProfitBTC = -1


		self.coins.sort(key=lambda x: x.ProfitBTC, reverse=True)

	def Print(self):

		for myCoin in self.coins:
			myCoin.Print()

	def MineMostProfitable(self):
		CoinToMine = self.coins[0]
		print("\tAttempt to start mining ", CoinToMine.FullName)
		if CoinToMine.ActiveMining:
			print("\t", CoinToMine.FullName, " is allraedy mining")
			with open(LogFileName, "a") as myfile:
				myfile.write("{0:s}\tcontinue\t{1:s}\t{2:8.6f}\t{3:8.6f}\n".format(datestr(), CoinToMine.Name, CoinToMine.Profit, CoinToMine.ProfitBTC))
		else:
			stopped = False
			number_running = 0
			for myCoin in self.coins:
				if myCoin.ActiveMining:
					number_running += 1
					if (time.time() - myCoin.ActiveMiningTime) < myCoin.MinimumMineTime:
						print("\tTo short time to stop mining ", myCoin.FullName)
						with open(LogFileName, "a") as myfile:
							myfile.write("{0:s}\tcontinue time\t{1:s}\t{2:8.6f}\t{3:8.6f}\n".format(datestr(), myCoin.Name, myCoin.Profit, myCoin.ProfitBTC))
					else:
						myCoin.StopMining()
						stopped = True
						print("\tAttempt to stop mining ", myCoin.FullName)
			if number_running == 0:
				stopped = True
			print(number_running, stopped)
			if stopped:
				CoinToMine.StartMining()
				print("\tStart mining ", CoinToMine.FullName)
				print()
