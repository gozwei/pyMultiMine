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
		self.DebugTarget = 3
		self.DanationCount = 0;

	def AddCoin(self, coin):
		self.coins.append(coin)

	def SetDryRun(self):
		self.DryRun = True

	def SetDebugTarget(self, DebugTarget):
		self.DebugTarget = DebugTarget

	def PrintDonationMsg(self):
		if self.DanationCount %10 == 0:
			Common.Log("MSG: If you find this software usefull, plese say thank you by donating some BTC:")
			Common.Log("MSG: 1DMcHCDus3izk7ia54R6BJfhDaf4visgnT")
		self.DanationCount += 1

	def GetBTCUSD(self):
		self.PrintDonationMsg()
		try:
			Common.Log("DEBUG: MultiMine.GetBTCUSD() 001", target=self.DebugTarget)
			html = Common.GetURL("https://api.cryptowat.ch/markets/kraken/btcusd/price", DebugTarget=self.DebugTarget)
			Common.Log("DEBUG: MultiMine.GetBTCUSD() 002", target=self.DebugTarget)
			data = json.loads(html)
			Common.Log("DEBUG: MultiMine.GetBTCUSD() 003", target=self.DebugTarget)
			self.BTCUSD = float(data["result"]["price"])
		except:
			Common.Log("ERROR: BTC/USD fetch failed")
			pass
		Common.Log("BTC/USD: {0:8.4f}".format(self.BTCUSD))

	def GetCoinStats(self):
		Common.Log("DEBUG: MultiMine.GetCoinStats() 001", target=self.DebugTarget)
		html = Common.GetURL("https://www.whattomine.com/coins.json", DebugTarget=self.DebugTarget)
		Common.Log("DEBUG: MultiMine.GetCoinStats() 002", target=self.DebugTarget)
		if html != "Error":
			Common.Log("DEBUG: MultiMine.GetCoinStats() 003", target=self.DebugTarget)
			try:
				data = json.loads(html)
			except:
				data = []
				Common.Log("ERROR: JSON parse failed")
			Common.Log("DEBUG: MultiMine.GetCoinStats() 004", target=self.DebugTarget)
			for myCoin in self.coins:
				try:
					Difficulty = data["coins"][myCoin.FullName]["difficulty"] 
					BlockTime = float(data["coins"][myCoin.FullName]["block_time"])
					NetHashRate =float(data["coins"][myCoin.FullName]["nethash"])
					BlockSize = data["coins"][myCoin.FullName]["block_reward"] 
					Price = data["coins"][myCoin.FullName]["exchange_rate"] 
					myCoin.SetMiningParameters(Difficulty, BlockTime, NetHashRate, BlockSize, Price)

					myCoin.CalcProfit()

					Common.Log("Profit 24h: {0:6s}{1:12.6f}{2:12.6f}\t${3:0,.2f}".format(myCoin.Name, myCoin.Profit, myCoin.ProfitBTC, myCoin.ProfitBTC*self.BTCUSD))
				except:
					Common.Log("ERROR: Coin {0} profit calculation failed".format(myCoin.Name))
					myCoin.Profit = -1
					myCoin.ProfitBTC = -1
		else:
			Common.Log("DEBUG: MultiMine.GetCoinStats() 005", target=self.DebugTarget)
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
						myCoin.StopMining(self.DryRun, DebugTarget=self.DebugTarget)
						stopped = True
						Common.Log("Attempt to stop mining ", myCoin.FullName)
			if number_running == 0:
				stopped = True
			if stopped:
				CoinToMine.StartMining(self.DryRun, DebugTarget=self.DebugTarget)
				Common.Log("Start mining ", CoinToMine.FullName)
