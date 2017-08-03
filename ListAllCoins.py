from MultiMineCommon import Common
import collections
import json

AllCoins = dict()
html = Common.GetURL("https://www.whattomine.com/coins.json")
if html != "Error":
	data = json.loads(html)
	for coin in data["coins"]:
		if "Nicehash" not in coin:
			AllCoins[data["coins"][coin]["tag"]] = coin

AllCoins = collections.OrderedDict(sorted(AllCoins.items()))
for k, v in AllCoins.items():
	print(k,":",v)
