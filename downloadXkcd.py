#!/usr/bin/env python3

# Morgan Wilkinson
# 07/26/2019

# This program is menant to traverse the XKCD site and download the comics there

import requests, os, bs4

# Starting URL
url = 'http://xkcd.com'

# store comics in ./xkcd
os.makedirs('xkcd', exist_ok=True)

while not url.endswith('#'):
	# TODO: Download the page.
	print("Downloading page %s..." % url)
	res = requests.get(url)
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text)

	# TODO: Find the URL of the comic image.
	comicElem = soup.select("#comic img")
	if comicElem == []:
		print("Could not find comic image.")

	else:
		try:
			comicUrl = 'http:' + comicElem[0].get('src')
			# TODO: Download the image.
			print('Downloading image %s...' % (comicUrl))
			res = requests.get(comicUrl)
			res.raise_for_status()
ç
		except requests.exceptions.MissingSchema:
			# Skip this comic
			prevLink = soup.select('a[rel="prev"]')[0]
			url = "http://xkcd.com" + prevLink.get('href')
			continue

		# TODO: Save the image to ./xkcd.
		imageFile = open(os.path.join("xkcd", os.path.basename(comicUrl)), 'wb')
		for chunk in res.iter_content(100000):
			imageFile.write(chunk)
		imageFile.close

	# TODO: Get the Prev button's url.
	prevLink = soup.select('a[rel="prev"]')[0]
	url = 'http://xkcd.com' + prevLink.get('href')
print('Done.')