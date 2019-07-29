#!/usr/bin/env python3

# Morgan Wilkinson
# 07/26/2019

# This program is meant to download the novels from wuxiaworld.com

import requests, os, bs4, pdfkit

os.chdir("/Users/morgan/Desktop")
# Ensure folder exist if not create it
os.makedirs("Spirit Realm", exist_ok=True)

def chapters():
	# Starting url
	url = "https://www.wuxiaworld.com/novel/spirit-realm/sr-chapter-1"

	#Download the page.
	index = 1
	while not index == 1533:
		# Download page
		print("Downloading page %s. . . " % url)
		res = requests.get(url)
		res.raise_for_status()

		# Convert page request to BeautifulSoup object
		soup = bs4.BeautifulSoup(res.text, 'html.parser')

		# Grab the chapter content
		chapElem = soup.find("div", {"class": "fr-view"})

		# Throw error if no chapter
		if chapElem == []:
			print("Could not find chapter.")
		else:
			chapter = '\n\n'.join(p.text for p in chapElem.findAll("p"))
			# Name the page a prepare it for writinf to.
			file = open(os.path.join("Spirit Realm", os.path.basename(url+".txt")), 'w')
			#change file to utf-8 with bom
			file.write('\ufeff') 
			 #write actual content to the file
			file.write(chapter)
			file.close()

		# Grab next page link.
		nextLink = chapElem.find("a", string="\nNext Chapter\n")
		url = "https://www.wuxiaworld.com" + nextLink.get('href')
		index += 1


def convertToPdf():
	for filename in os.listdir("/users/morgan/desktop/Spirit Realm"):
		if filename.endswith('.txt'):
			with open(os.path.join("/users/morgan/desktop/Spirit Realm", filename), 'r') as f:
				pdfkit.from_file(f, str(filename)+'.pdf')


