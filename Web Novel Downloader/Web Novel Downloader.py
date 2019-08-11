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
import shutil  
import time
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QFileDialog, QCheckBox
from webNovelDownloaderInterface import Ui_webNovelDownloader

wuxiaworldDict = {"A Record of a Mortal’s Journey to Immortality":"rmji/rmji-chapter-", "A Will Eternal":"a-will-eternal/awe-chapter-", "Against the Gods":"against-the-gods/atg-chapter-", "Ancient Strengthening Technique":"ancient-strengthening-technique/ast-chapter-",
					"Archfiend":"archfiend/af-chapter-", "Battle Through the Heavens":"battle-through-the-heavens/btth-chapter-", "Dragon Maken War":"dragon-maken-war/dmw-chapter-",
					"Dragon Prince Yuan":"dragon-prince-yuan/yz-chapter-", "Emperor’s Domination":"emperors-domination/emperor-chapter-", "Gate of Revelation":"gate-of-revelation/gor-chapter-", "Heaven's Devourer":"heavens-devourer/hd-chapter-",
					"I Reincarnated For Nothing":"i-reincarnated-for-nothing/irfn-chapter-", "Imperial God Emperor":"imperial-god-emperor/ige-chapter-", "Invincible":"invincible/inv-chapter-", "Legend of the Dragon King":"legend-of-the-dragon-king/ldk-chapter-",
					"Martial God Asura":"martial-god-asura/mga-chapter-", "Martial World":"martial-world/mw-chapter-", "Nine Star Hegemon Body Art":"nine-star-hegemon/nshba-chapter-", "Overgeared":"overgeared/og-chapter-", "Perfect World":"perfect-world/pw-chapter-",
					"Rebirth of the Thief Who Roamed the World":"rebirth-of-the-thief-who-roamed-the-world/rotwrtw-chapter-", "Renegade Immortal":"renegade-immortal/rge-chapter-", "Sage Monarch":"sage-monarch/sm-chapter-", "Skyfire Avenue":"skyfire-avenue/sfl-chapter-",
					"Sovereign of the Three Realms":"sovereign-of-the-three-realms/sotr-chapter-", "Spirit Realm":"spirit-realm/sr-chapter-", "Spirit Vessel":"spirit-vessel/sv-chapter-", "Stop, Friendly Fire!":"stop-friendly-fire/sff-chapter-", "Talisman Emperor":"talisman-emperor/te-chapter-",
					"The Great Ruler":"the-great-ruler/tgr-chapter-", "The Novel's Extra":"the-novels-extra/tne-chapter-", "Trash of the Count's Family":"trash-of-the-counts-family/tcf-chapter-", "Warlock of the Magus World":"warlock-of-the-magus-world/wmw-chapter-",
					"Wu Dong Qian Kun":"wu-dong-qian-kun/wdqk-chapter-"}

class WebNovelDownloader(Ui_webNovelDownloader):
	def __init__(self, dialog):
		Ui_webNovelDownloader.__init__(self)
		self.setupUi(dialog)

		# Buttons, Entry Boxes, Check Boxes and etc functionality.

		#Add novels to choose from
		for key, value in wuxiaworldDict.items():
			self.novelMenu.addItem(key, value)
			
		self.openDirectory.clicked.connect(self.setFilePath)
		self.startButton.clicked.connect(self.chapters)
		
	# Get the file path using the openDirectory button
	def setFilePath(self):
		filePath = QFileDialog.getExistingDirectory()
		# Make filePath current directory
		filePath = filePath+"/"+self.novelMenu.currentText()
		# Should make when hit start----------------------
		self.directoryPath.setText(os.path.abspath(filePath))

	# This method deletes multiple files in the filePath.
	def deleteAllFiles(self, filePath):
		if os.path.exists(filePath) == True:
			send2trash.send2trash(filePath)
		else:
			self.statusbar.showMessage("Path does not exist! Continuing!")

	# This method deletes multiple files of the same type in the filePath.
	def deleteExtFiles(self, convertedFilePath, fileType):
		convertedFilePath = convertedFilePath+"PDF/"
		if os.path.exists(convertedFilePath) == True:
			for filename in os.listdir(convertedFilePath):
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
		pdfFiles = sorted(pdfFiles, key=lambda item: (int(item.partition('.')[0]) if item[0].isdigit() else float('inf'), item))
		
		# Create a pdfFileWriter 
		pdfWriter = PyPDF2.PdfFileWriter()

		index = 1
		# For each file in the pdfFiles list open it and create a pdfFileReader object.
		for filename in pdfFiles:
			self.statusbar.showMessage("Adding %s to the master PDF file!" % filename)
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
		self.statusbar.showMessage("Done go enjoy your novel!")

	# Convert files in path folder
	def convertToPdf(self, convertedFilePath, convertPDFChecked, pdfMergeChecked):
		os.chdir(convertedFilePath)
		pdfPath = convertedFilePath+"PDF/"
		os.makedirs(pdfPath, exist_ok=True)
		config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
		for filename in os.listdir("."):
			if filename.endswith(".txt"):
				self.statusbar.showMessage("Converting file %s to PDF format!" % filename)
				# Convert to PDF
				pdfkit.from_file(filename, pdfPath+(os.path.splitext(filename)[0])+".pdf", configuration = config) 

		if pdfMergeChecked == 1:
			# Call pdfMerge once all files have been converted to pdf
			self.pdfMerge(pdfPath)
			if convertPDFChecked == 0:
				self.deleteExtFiles(convertedFilePath, ".pdf")
				self.statusbar.showMessage("Done go enjoy your novel!")
		else:
			self.statusbar.showMessage("Done go enjoy your novel!")

	# Get chapter content and process it.
	def chapters(self):
		# Starting url
		novelIndex = self.novelMenu.currentIndex()
		novelUrlExt = self.novelMenu.itemData(novelIndex)
		url = "https://www.wuxiaworld.com/novel/"+novelUrlExt
		delay = 25
		convertPDFChecked = 0
		pdfMergeChecked = 0
		filePath = self.directoryPath.text()+"/"

		if self.deleteFiles.isChecked():
			self.deleteAllFiles(self.directoryPath.text())
			os.makedirs(filePath, exist_ok=True)
		os.makedirs(filePath, exist_ok=True)

		if self.convertPDF.isChecked():
			# for text files
			convertedFilePath = filePath+"Converted/"
			os.makedirs(convertedFilePath, exist_ok=True)

			writeTo = convertedFilePath
			#Set the marker
			convertPDFChecked = 1

			if self.combinePDF.isChecked():
				#Set the marker
				pdfMergeChecked = 1
			#convertPDF on but combinePDF off
			else: 
				#Set the marker
				pdfMergeChecked = 0

		elif self.convertPDF.isChecked() == False:
			#Set the marker
			convertPDFChecked = 0
			if self.combinePDF.isChecked():
				# for text files
				convertedFilePath = filePath 
				os.makedirs(convertedFilePath, exist_ok=True)

				writeTo = convertedFilePath
				#Set the marker
				pdfMergeChecked = 1

			else:
				writeTo = filePath

		# Check to see if there is a stated amount of files to download
		index = self.chapterIndexStart.value()

		if self.latestChapter.isChecked():
			endIndex = 15000 #### Fix
		else:
			endIndex = self.chapterIndexEnd.value()

		if index > endIndex:
			self.statusbar.showMessage("Error start index must be larger than the ending index!")

		else:
			for urlNumber in range(index, endIndex + 1):
				# Download page
				self.statusbar.showMessage("Downloading page %s. . . " % urlNumber)
				res = requests.get(url+"%s" % (urlNumber) )
				
				try:
					res.raise_for_status()
				except:
					self.statusbar.showMessage("No chapter found!")

				# Convert page request to BeautifulSoup object
				soup = bs4.BeautifulSoup(res.text, 'html.parser')

				# Grab the chapter content
				chapElem = soup.find("div", class_="p-15")

				# Remove unwanted teaser.
				try:
					remove = chapElem.find("p", {"style": "text-align: center"})
					remove.clear()
				except:
					self.statusbar.showMessage("No teaser found!")

				# Throw error if no chapter
				if chapElem == []:
					self.statusbar.showMessage("Could not find chapter content!")
				else:
					# Get the file name
					chapterName = str(urlNumber)
					# Insert newlines
					chapter = '\n\n'.join(p.text for p in chapElem.findAll("p"))
					# Name the page a prepare it for writing to.
					file = open(os.path.join(writeTo, chapterName+".txt"), 'w')
					#change file to utf-8 with bom
					file.write('\ufeff') 
					 #write the actual content to the file
					file.write(chapter)
					file.close()

				index += 1
				# Ease webscrapping burden
				if index % 20 == 0:
					self.statusbar.showMessage("Delay every 20 chapters! Dont get banned!", delay)
					time.sleep(delay)

		if convertPDFChecked == 1 or pdfMergeChecked == 1:
			threadObj = threading.Thread(target=self.convertToPdf, args=[writeTo, convertPDFChecked, pdfMergeChecked])
			threadObj.start()
		else:
			self.statusbar.showMessage("Done go enjoy your novel!")


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	dialog = QtWidgets.QMainWindow()
	program = WebNovelDownloader(dialog)
	dialog.show()
	sys.exit(app.exec_())






