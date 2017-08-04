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
		Common.Log("DEBUG: MultiMine.GetBTCUSD() 001")
		html = Common.GetURL("https://api.cryptowat.ch/markets/kraken/btcusd/price")
		Common.Log("DEBUG: MultiMine.GetBTCUSD() 002")
		data = json.loads(html)
		Common.Log("DEBUG: MultiMine.GetBTCUSD() 003")
		self.BTCUSD = float(data["result"]["price"])
		Common.Log("BTC/USD: {0:8.4f}".format(self.BTCUSD))

	def GetCoinStats(self):
		Common.Log("DEBUG: MultiMine.GetCoinStats() 001")
		html = Common.GetURL("https://www.whattomine.com/coins.json")
		Common.Log("DEBUG: MultiMine.GetCoinStats() 002")
		if html != "Error":
			Common.Log("DEBUG: MultiMine.GetCoinStats() 003")
			data = json.loads(html)
			Common.Log("DEBUG: MultiMine.GetCoinStats() 004")
			for myCoin in self.coins:
				Difficulty = data["coins"][myCoin.FullName]["difficulty"] 
				BlockTime = float(data["coins"][myCoin.FullName]["block_time"])
				NetHashRate =float(data["coins"][myCoin.FullName]["nethash"])
				BlockSize = data["coins"][myCoin.FullName]["block_reward"] 
				Price = data["coins"][myCoin.FullName]["exchange_rate"] 
				myCoin.SetMiningParameters(Difficulty, BlockTime, NetHashRate, BlockSize, Price)

				myCoin.CalcProfit()

				Common.Log("Profit 24h: {0:6s}{1:12.6f}{2:12.6f}\t${3:0,.2f}".format(myCoin.Name, myCoin.Profit, myCoin.ProfitBTC, myCoin.ProfitBTC*self.BTCUSD))
		else:
			Common.Log("DEBUG: MultiMine.GetCoinStats() 005")
			for myCoin in self.coins:
				if myCoin.Default:
					myCoin.Profit = 0
					myCoin.ProfitBTC = 0
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
			Common.Log("Continue: {0:6s}{1:12.6f}{2:12.6f}\t${3:0,.2f}".format(CoinToMine.Name, CoinToMine.Profit, CoinToMine.ProfitBTC, CoinToMine.ProfitBTC*self.BTCUSD))
		else:
			stopped = False
			number_running = 0
			for myCoin in self.coins:
				myCoin.SetBTCUSD(self.BTCUSD)
				if myCoin.ActiveMining:
					number_running += 1
					if (time.time() - myCoin.ActiveMiningTime) < myCoin.MinimumMineTime:
						Common.Log("To short time to stop mining ", myCoin.FullName)
						Common.Log("Continue time: {0:6s}{1:12.6f}{2:12.6f}\t${3:0,.2f}".format(myCoin.Name, myCoin.Profit, myCoin.ProfitBTC, myCoin.ProfitBTC*self.BTCUSD))
					else:
						myCoin.StopMining(self.DryRun)
						stopped = True
						Common.Log("Attempt to stop mining ", myCoin.FullName)
			if number_running == 0:
				stopped = True
			if stopped:
				CoinToMine.StartMining(self.DryRun)
				Common.Log("Start mining ", CoinToMine.FullName)
