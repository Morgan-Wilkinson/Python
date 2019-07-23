# Morgan Wilkinson
# 07/21/2019

# This program deals with compressing files using the ZipFile Module

import zipfile, os

os.chdir("/Users/morgan/Desktop")
exampleZip = zipfile.ZipFile("TimeSheets.zip")
exampleZip.namelist()
