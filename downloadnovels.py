#!/usr/bin/env python3

# Morgan Wilkinson
# 07/26/2019

# This program is meant to download the novels from wuxiaworld.com

import bs4, os, pdfkit, PyPDF2, requests, send2trash, sys 

# Make Desktop current directory 
os.chdir("/Users/morgan/Desktop/")
# Ensure folder exist if not create it.
filePath = "/Users/morgan/Desktop/Spirit Realm/"
pdfPath = filePath+"PDF/"

os.makedirs(filePath, exist_ok=True)
os.makedirs(pdfPath, exist_ok=True)

# This method deletes multiple files of the same type.
def deleteFiles(fileType):
	for filename in os.listdir():
		if filename.endswith(fileType):
			print(filename)
			send2trash.send2trash(filename)

# Merge all PDFs into one PDF Book. This method retrieves ALL pdf files in the pdfPath and combines them.
# If you want only what was recently downloaded run the deletFiles function first.
def pdfMerge(pdfPath):
	# Move current directory to /Users/morgan/Desktop/Spirit Realm/PDF/
	os.chdir(pdfPath)

	# Deletes the file if it exists to avoid a invalid stream length error.
	if os.path.isfile(pdfPath+"Spirit Realm.pdf") == True:
		send2trash.send2trash("Spirit Realm.pdf")

	# Create an empty list
	pdfFiles = []
	# Search in the current directory for files ending with .pdf
	for filename in os.listdir('.'):
		if filename.endswith(".pdf"):
			# Add all found files to the list.
			pdfFiles.append(filename)
	# Sort the list
	pdfFiles.sort(key=str.lower)
	# Create a pdfFileWriter 
	pdfWriter = PyPDF2.PdfFileWriter()

	index = 1
	# For each file in the pdfFiles list open it and create a pdfFileReader object.
	for filename in pdfFiles:
		print("Adding %s to the master PDF file!" % filename)
		pdfFileObj = open(filename, 'rb')
		pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

		for pageNum in range(0, pdfReader.numPages):
			# Add all found pdf pages to the pdfWriter object.
			pageObj = pdfReader.getPage(pageNum)
			pdfWriter.addPage(pageObj)
		
		# Offset to account of pageNum starting at 0.
		offset = 1
		# Bookmark for each page is chapter is calculated by taking the total number of pages and subtracting it from the chapter length.
		bookmarkPage = pdfWriter.getNumPages() - offset - pageNum
		pdfWriter.addBookmark("Chapter "+str(index), bookmarkPage)
		index += 1

	# Save the results.
	pdfOutput = open('Spirit Realm.pdf', 'wb')
	pdfWriter.write(pdfOutput)
	pdfOutput.close()

# Convert files in path folder
def convertToPdf(filePath, pdfPath):
	os.chdir(filePath)
	for filename in os.listdir():
		if filename.endswith(".txt"):
			print("Converting file %s to PDF format!" % filename)
			output = (os.path.splitext(filename)[0])
			pdfkit.from_file(filePath+filename, pdfPath+output+".pdf")

	# Call pdfMerge once all files have been converted to pdf
	pdfMerge(pdfPath)

# Get chapter content and process it.
def chapters():
	# Starting url
	url = "https://www.wuxiaworld.com/novel/spirit-realm/sr-chapter-1"

	# Check to see if there is a stated amount of files to download
	if len(sys.argv) > 1:
		desired = ' '.join(sys.argv[1:])
	else:
		desired = 5

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

# Starts off the process. The root basically.
chapters()



