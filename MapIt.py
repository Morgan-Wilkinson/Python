#!/usr/bin/env python3

# Morgan Wilkinson
# 07/21/2019

# mapIt.py - Launches a map in the browser using an address from the
# command line or clipboard.
# To run the program do ./MapIt.py whatever address you want

import webbrowser, sys, pyperclip

if len(sys.argv) > 1:
	# Get address from command line
	address = ' '.join(sys.argv[1:])

else:
	# Get address from clipboard
	address = pyperclip.paste()

webbrowser.open("https://www.google.com/maps/place/" + address)