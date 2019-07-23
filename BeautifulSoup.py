# Morgan Wilkinson
# 07/23/2019

# This program downloads files from the web using the request module.

import requests, bs4

res = requests.get("http://nostrach.com")
try:
	res.raise_for_status()
except Exception as exc:
	print("Fatal Error %s" % (exc))

noStarchSoup = bs4.BeautifulSoup(res.text)
type(noStarchSoup)
