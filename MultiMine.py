import json
import urllib.request
from time import sleep
import shlex, subprocess
import time
import datetime
from MultiMineCommon import Common

class MultiMine():
	def __init__(self):
		Common.Log('Multi Miner initiated')
		self.coins = []
		self.BTCUSD = 0
		self.DryRun = False

	def AddCoin(self, coin):
		self.coins.append(coin)

	def SetDryRun(self):
		self.DryRun = True

	def GetBTCUSD(self):
		html = Common.GetURL("https://api.cryptowat.ch/markets/kraken/btcusd/price")
		data = json.loads(html)
		self.BTCUSD = float(data["result"]["price"])
		Common.Log("BTC/USD: {0:8.4f}".format(self.BTCUSD))

	def GetCoinStats(self):
		html = Common.GetURL("https://www.whattomine.com/coins.json")
		if html != "Error":
			data = json.loads(html)
			for myCoin in self.coins:
				Difficulty = data["coins"][myCoin.FullName]["difficulty"] 
				BlockTime = float(data["coins"][myCoin.FullName]["block_time"])
				NetHashRate =float(data["coins"][myCoin.FullName]["nethash"])
				BlockSize = data["coins"][myCoin.FullName]["block_reward"] 
				Price = data["coins"][myCoin.FullName]["exchange_rate"] 
				myCoin.SetMiningParameters(Difficulty, BlockTime, NetHashRate, BlockSize, Price)

				myCoin.CalcProfit()

				Common.Log("Profit 24h: {0:6s}\t{1:12.6f}\t{2:12.6f}\t{3:12.6f}$".format(myCoin.Name, myCoin.Profit, myCoin.ProfitBTC, myCoin.ProfitBTC*self.BTCUSD))
		else:
			for myCoin in self.coins:
				if myCoin.Default:
					myCoin.Profit = 0
					myCoin.ProfitBTC = 0
					# with open(LogFileName, "a") as myfile:
					# 	myfile.write("{0:s}\terror fetching data, mining default\t{1:s}\n".format(datestr(), myCoin.Name))
				else:
					myCoin.Profit = -1
					myCoin.ProfitBTC = -1


		self.coins.sort(key=lambda x: x.ProfitBTC, reverse=True)

	def Print(self):

		for myCoin in self.coins:
			myCoin.Print()

	def MineMostProfitable(self):
		CoinToMine = self.coins[0]
		Common.Log("Attempt to start mining " + CoinToMine.FullName)
		if CoinToMine.ActiveMining:
			Common.Log(CoinToMine.FullName + " is already mining")
			# with open(LogFileName, "a") as myfile:
			# 	myfile.write("{0:s}\tcontinue\t{1:s}\t{2:8.6f}\t{3:8.6f}\n".format(datestr(), CoinToMine.Name, CoinToMine.Profit, CoinToMine.ProfitBTC))
			Common.Log("Continue: {0:6s}\t{1:12.6f}\t{2:12.6f}\t{3:12.6f}$".format(CoinToMine.Name, CoinToMine.Profit, CoinToMine.ProfitBTC, CoinToMine.ProfitBTC*self.BTCUSD))
		else:
			stopped = False
			number_running = 0
			for myCoin in self.coins:
				if myCoin.ActiveMining:
					number_running += 1
					if (time.time() - myCoin.ActiveMiningTime) < myCoin.MinimumMineTime:
						Common.Log("To short time to stop mining ", myCoin.FullName)
						# with open(LogFileName, "a") as myfile:
						# 	myfile.write("{0:s}\tcontinue time\t{1:s}\t{2:8.6f}\t{3:8.6f}\n".format(datestr(), myCoin.Name, myCoin.Profit, myCoin.ProfitBTC))
						Common.Log("Continue time: {0:6s}\t{1:12.6f}\t{2:12.6f}\t{3:12.6f}$".format(myCoin.Name, myCoin.Profit, myCoin.ProfitBTC, myCoin.ProfitBTC*self.BTCUSD))
					else:
						myCoin.StopMining(self.DryRun)
						stopped = True
						Common.Log("Attempt to stop mining ", myCoin.FullName)
			if number_running == 0:
				stopped = True
			if stopped:
				CoinToMine.StartMining(self.DryRun)
				Common.Log("Start mining ", CoinToMine.FullName)
