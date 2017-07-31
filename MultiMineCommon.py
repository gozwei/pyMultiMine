import json
import urllib.request
from time import sleep
import shlex, subprocess
import time
import datetime

class Common():
	def datestr(format="std"):
		ts = time.time()
		if format == "file":
			return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
		else:
			return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

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