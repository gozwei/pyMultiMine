import json
import urllib.request
from time import sleep
import shlex, subprocess
import time
import datetime

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
		else:
			return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

	def Log(message, target=3):
		if target == 1 or target == 3:
			LogFileName = Common.datestr(format="file")
			with open(LogFileName, "a") as myfile:
				myfile.write(message + "\n")
		if target == 2 or target == 3: 
			print(bcolors.OKBLUE + bcolors.BOLD + "[{0:s}] ".format(Common.datestr()) + message + bcolors.ENDC)

	def GetURL(url):
		try:
			hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
				   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
				   'Accept-Encoding': 'none',
				   'Accept-Language': 'en-US,en;q=0.8',
				   'Connection': 'keep-alive'}

			response = urllib.request.Request(url,headers=hdr)
			response = urllib.request.urlopen(response)
			html = response.read()
			return str(html.decode('UTF-8'))
		except:
			return "Error"