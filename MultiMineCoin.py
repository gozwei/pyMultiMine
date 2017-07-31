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

	def StartMining(self):
		if self.ActiveMining == False:
			sleep(3)
			self.ActiveMining = True
			args = shlex.split(self.executable)
			self.process = subprocess.Popen(args)
			with open(LogFileName, "a") as myfile:
				myfile.write("{0:s}\tstart\t{1:s}\t{2:8.6f}\t{3:8.6f}\n".format(datestr(), self.Name, self.Profit, self.ProfitBTC))
			self.ActiveMiningTime = time.time()

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
		self.Profit = D * 1440
		self.ProfitBTC = E

	def Print(self):
		print(self.Name, self.Profit)
