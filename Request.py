# Morgan Wilkinson
# 07/21/2019

#Requests - This program downloads files from the web using the request module.

import requests

res = requests.get("https://automatetheboringstuff.com/files.txt")
type(res)
try:
	res.raise_for_status()
except Exception as exc:
	print("There was a problem: %s" % (exc))

len(res.text)
print(res.text[:250])
