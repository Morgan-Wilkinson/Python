#!/usr/bin/env python3

# Morgan Wilkinson
# 07/26/2019

# This program is meant to download the novels from wuxiaworld.com

import bs4
import os
import pdfkit
import PyPDF2
import requests
import send2trash 
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QCheckBox
from webNovelDownloaderInterface import Ui_webNovelDownloader

class WebNovelDownloader(Ui_webNovelDownloader):
	def __init__(self, dialog):
		Ui_webNovelDownloader.__init__(self)
		self.setupUi(dialog)

		# Buttons, Entry Boxes, Check Boxes and etc functionality.
		self.openDirectory.clicked.connect(self.setFilePath)
		self.startButton.clicked.connect(self.chapters)
		

	def setFilePath(self):
		filePath = QFileDialog.getExistingDirectory()
		# Make filePath current directory
		filePath = filePath+"/Spirit Realm"
		# Should make when hit start----------------------
		os.makedirs(filePath, exist_ok=True)
		os.chdir(filePath)
		self.directoryPath.setText(os.path.abspath(filePath))


	# This method deletes multiple files in the filePath.
	def deleteAllFiles(self, filePath):
		if os.path.exists(filePath) == True:
			send2trash.send2trash(filePath)

	def deleteExtFiles(self, filePath, fileType):
		deletionPath = filePath+"PDF/"
		if os.path.exists(deletionPath) == True:
			for filename in os.listdir(deletionPath):
				if filename.endswith(fileType):
					if filename.startswith("Complete"):
						continue
					else:
						send2trash.send2trash(filename)

	# Merge all PDFs into one PDF Book. This method retrieves ALL pdf files in the pdfPath and combines them.
	# If you want only what was recently downloaded run the deletFiles function first.
	def pdfMerge(self, pdfPath):
		os.chdir(pdfPath)

		# Deletes the file if it exists to avoid a invalid stream length error.
		if os.path.isfile(pdfPath+"Complete.pdf") == True:
			send2trash.send2trash("Complete.pdf")

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
		pdfOutput = open('Complete.pdf', 'wb')
		pdfWriter.write(pdfOutput)
		pdfOutput.close()

	# Convert files in path folder
	def convertToPdf(self, filePath, number):
		os.chdir(filePath)
		pdfPath = filePath+"PDF/"
		os.makedirs(pdfPath, exist_ok=True)

		for filename in os.listdir("."):
			if filename.endswith(".txt"):
				print("Converting file %s to PDF format!" % filename)
				output = (os.path.splitext(filename)[0])
				pdfkit.from_file(filePath+filename, pdfPath+output+".pdf")

		if number == 1:
			# Call pdfMerge once all files have been converted to pdf
			self.pdfMerge(pdfPath)
		else:
			print("Done!")

	# Get chapter content and process it.
	def chapters(self):
		filePath = self.directoryPath.text()+"/"

		if self.deleteFiles.isChecked():
			self.deleteAllFiles(self.directoryPath.text())

		os.makedirs(filePath, exist_ok=True)

		# Starting url
		url = "https://www.wuxiaworld.com/novel/spirit-realm/sr-chapter-1"

		# Check to see if there is a stated amount of files to download
		startIndex = self.chapterIndexStart.value()

		if self.latestChapter.isChecked():
			endIndex = 15000 #### Fix
		else:
			endIndex = self.chapterIndexEnd.value()

		if startIndex > endIndex:
			print("error") #########Set status bar to print message

		else:
			while not startIndex == endIndex:
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
					file = open(os.path.join(filePath, chapterName+".txt"), 'w')
					#change file to utf-8 with bom
					file.write('\ufeff') 
					 #write the actual content to the file
					file.write(chapter)
					file.close()

				# Grab next page link.
				nextLink = chapElem.find("a", string="\nNext Chapter\n")
				url = "https://www.wuxiaworld.com" + nextLink.get('href')

				startIndex += 1
		
		print(self.convertPDF.isChecked())
		if self.convertPDF.isChecked():
			if self.combinePDF.isChecked():
				self.convertToPdf(filePath, 1)
			else:
				self.convertToPdf(filePath, 0)

		elif self.convertPDF.isChecked() == False:
			if self.combinePDF.isChecked():
				self.convertToPdf(filePath, 1)
				self.deleteExtFiles(filePath, ".pdf")


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	dialog = QtWidgets.QMainWindow()
	program = WebNovelDownloader(dialog)
	dialog.show()
	sys.exit(app.exec_())

