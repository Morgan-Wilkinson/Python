#!/usr/bin/env python3

# Morgan Wilkinson
# 07/23/2019

# I'm Lucky the worlds most magical program... Seriously though this program takes input from the
# command line and then preforms a google search and open the top search results in another tab

import sys, webbrowser, requests, bs4
print(sys.version)
# Prints googling while searching
print("Googling...")

# Creates the base URL for searching on google
res = requests.get('https://www.google.com/search?q=' + ' '.join(sys.argv[1:]))

# In the event of a page not being valid raise an exception 
try:
    res.raise_for_status()
except Exception as exc:
    print("Fatal Error: %s" % (exc))

# Retrive the top search result links
soup = bs4.BeautifulSoup(res.text, "html.parser")

# Open a browser tab for each result
linkElems = soup.select('div#main > div > div > div > a')

numOpen = min(5, len(linkElems))
for i in range(numOpen):
	webbrowser.open('http://google.com' + linkElems[i].get('href'))