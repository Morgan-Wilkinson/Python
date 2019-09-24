#!/usr/bin/env python3
# Morgan Wilkinson
# 07/23/2019

# This program parsers RSS and returns the top 10 headline news from Top Stories - CNN.

import sys
import requests
import bs4

if len(sys.argv) > 1:
	url = "http://rss.cnn.com/rss/edition_"+"".join(sys.argv[1:])+".rss"
	print(url)
else:
	url = "http://rss.cnn.com/rss/edition.rss"

res = requests.get(url)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text)
print(soup)

headlines = soup.find_all('li')
print(headlines)

