import requests, os, bs4
from bs4 import UnicodeDammit
import pdfkit

os.chdir("/Users/morgan/Desktop")
# Ensure folder exist if not create it

options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'custom-header' : [
        ('Accept-Encoding', 'gzip')
    ]
}

pdfkit.from_file("sr-chapter-1.txt", "ou2.pdf", options=options)