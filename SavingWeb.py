# Morgan Wilkinson
# 07/22/2019

# SavingWeb - This program downloads files from the web using the request module.

import requests

res = requests.get("https://creativenovels.com/73/chapter-120-are-you-expecting/")
try:
	res.raise_for_status()
except Exception as exc:
	print("Fatal Error: %s" % (exc))

playFile = open("Test.html", 'wb')
for chunk in res.iter_content(100000):
	playFile.write(chunk)

playFile.close()