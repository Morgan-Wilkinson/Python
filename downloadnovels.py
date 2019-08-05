#!/usr/bin/env python3

# Morgan Wilkinson
# 07/26/2019

# This program is meant to download the novels from wuxiaworld.com

import requests, sys, os, bs4, pdfkit

# Make Desktop current directory 
os.chdir("/Users/morgan/Desktop/")
# Ensure folder exist if not create it
filePath = "/Users/morgan/Desktop/Spirit Realm/"
pdfPath = filePath+"PDF/"

os.makedirs(filePath, exist_ok=True)
os.makedirs(pdfPath, exist_ok=True)


# Convert files in path folder
def convertToPdf(filePath, pdfPath):
	os.chdir(filePath)
	for filename in os.listdir():
		if filename.endswith(".txt"):
			output = (os.path.splitext(filename)[0])
			pdfkit.from_file(filePath+filename, pdfPath+output+".pdf")

def chapters():
	# Starting url
	url = "https://www.wuxiaworld.com/novel/spirit-realm/sr-chapter-1"

	# Check to see if there is a stated amount of files to download
	if len(sys.argv) > 1:
		desired = ' '.join(sys.argv[1:])
	else:
		desired = 10

	index = 1
	while not index == int(desired):
		# Download page
		print("Downloading page %s. . . " % url)
		res = requests.get(url)
		
		try:
			res.raise_for_status()
		except:
			print("No chapter found!")

		# Convert page request to BeautifulSoup object
		soup = bs4.BeautifulSoup(res.text, 'html.parser')

		# Grab the chapter content
		chapElem = soup.find("div", class_="p-15")

		# Remove unwanted teaser.
		try:
			remove = chapElem.find("p", {"style": "text-align: center"})
			remove.clear()
		except:
			print("No teaser found!")

		# Throw error if no chapter
		if chapElem == []:
			print("Could not find chapter content!")
		else:
			# Get the file name
			chapterName = os.path.basename(url)
			# Insert newlines
			chapter = '\n\n'.join(p.text for p in chapElem.findAll("p"))
			# Name the page a prepare it for writing to.
			file = open(os.path.join("Spirit Realm", chapterName+".txt"), 'w')
			#change file to utf-8 with bom
			file.write('\ufeff') 
			 #write the actual content to the file
			file.write(chapter)
			file.close()

		# Grab next page link.
		nextLink = chapElem.find("a", string="\nNext Chapter\n")
		url = "https://www.wuxiaworld.com" + nextLink.get('href')

		index += 1

	convertToPdf(filePath, pdfPath)

chapters()



