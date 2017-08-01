import json
import urllib.request
from time import sleep
import shlex, subprocess
import time
import datetime
from MultiMineCommon import Common

class Coin():
	def __init__(self, Name, FullName):
		self.Name = Name
		self.FullName = FullName
		self.Profit = 0
		self.ActiveMining = False
		self.Default = False
		self.MinimumMineTime = 3*60

	def SetAsDefault(self):
		self.Default = True

	def SetExecutable(self, executable):
		self.executable = executable

	def SetMinimumMineTime(self, MinimumMineTime):
		self.MinimumMineTime = MinimumMineTime

	def StartMining(self, DryRun):
		if self.ActiveMining == False:
			sleep(3)
			self.ActiveMining = True
			args = shlex.split(self.executable)
			if not DryRun:
				self.process = subprocess.Popen(args)
			Common.Log("Start: {0:6s}\t{1:12.6f}\t{2:12.6f}".format(self.Name, self.Profit, self.ProfitBTC))
			self.ActiveMiningTime = time.time()

	def StopMining(self, DryRun):
		if self.ActiveMining == True:
			if not DryRun:
				self.process.terminate()
			self.ActiveMining = False
			Common.Log("Stop: {0:6s}".format(self.Name))

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
		self.Profit = D * 1440
		self.ProfitBTC = E

	def Print(self):
		print(self.Name, self.Profit)
