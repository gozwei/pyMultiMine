import json
import urllib.request
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


MyRates = dict()
MyRates["Equihash"] = 3.4e3
MyRates["Myriad-Groestl"] = 520e6
MyRates["LBRY"] = 2323e6



for coin in json1_data["coins"].items():
	CoinInfo = coin[1]
	CoinName = coin[0]
	if CoinInfo["algorithm"] in MyRates.keys():
		if CoinInfo["tag"] != "NICEHASH":
			CoinDifficulty = CoinInfo["difficulty"] 
			CoinBlockTime = float(CoinInfo["block_time"])
			CoinNetHashRate =float(CoinInfo["nethash"])
			MyHashRate = MyRates[CoinInfo["algorithm"]]
			CoinBlockSize = CoinInfo["block_reward"] 
			CoinPrice = CoinInfo["exchange_rate"] 
			BTC = 2550

			A = CoinDifficulty / CoinBlockTime
			B = MyHashRate / CoinNetHashRate
			C = (60 / CoinBlockTime) * CoinBlockSize
			D = B * C
			E = D * 1440 * CoinPrice
			Profit = E * BTC
			print(CoinName, E, Profit, sep="\t")
	else:
		pass
		#print(CoinName, CoinInfo["algorithm"])
#print(str(html).decode())