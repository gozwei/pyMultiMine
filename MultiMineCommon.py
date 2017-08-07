import json
import urllib.request
from time import sleep
import shlex, subprocess
import time
import datetime
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Common():
	def datestr(format="std"):
		ts = time.time()
		if format == "file":
			return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
		elif format == "ms":
			return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')
		else:
			return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

	def Log(message, target=3):
		# target = 0: Do not log message
		# target = 1: Log to file only
		# target = 2: Log to screen only
		# target = 3: Log to both file and screen (default)
		if target == 1 or target == 3:
			LogFileName = Common.datestr(format="file") + ".log"
			with open(LogFileName, "a") as myfile:
				myfile.write("[{0:s}] ".format(Common.datestr(format="ms")) + message + "\n")
		if target == 2 or target == 3: 
			if "ERROR:" in message:
				print(bcolors.FAIL + bcolors.BOLD + "[{0:s}] ".format(Common.datestr()) + message + bcolors.ENDC)
			elif "DEBUG:" in message:
				print(bcolors.YELLOW + bcolors.BOLD + "[{0:s}] ".format(Common.datestr()) + message + bcolors.ENDC)
			elif "MSG:" in message:
				print(bcolors.OKGREEN + bcolors.BOLD + bcolors.UNDERLINE + "[{0:s}] ".format(Common.datestr()) + message + bcolors.ENDC)
			else:
				print(bcolors.OKBLUE + bcolors.BOLD + "[{0:s}] ".format(Common.datestr()) + message + bcolors.ENDC)

	def GetURL(url, DebugTarget=1):
		Common.Log("DEBUG: Common.GetURL() 001:" + url, target=DebugTarget)
		try:
			hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
				   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
				   'Accept-Encoding': 'none',
				   'Accept-Language': 'en-US,en;q=0.8',
				   'Connection': 'keep-alive'}
			Common.Log("DEBUG: Common.GetURL() 002:" + url, target=DebugTarget)
			response = urllib.request.Request(url,headers=hdr)
			Common.Log("DEBUG: Common.GetURL() 003:" + url, target=DebugTarget)
			response = urllib.request.urlopen(response, timeout=3)
			Common.Log("DEBUG: Common.GetURL() 004:" + url, target=DebugTarget)
			html = response.read()
			Common.Log("DEBUG: Common.GetURL() 005:" + url, target=DebugTarget)
			return str(html.decode('UTF-8'))
		except:
			return "Error"
			
