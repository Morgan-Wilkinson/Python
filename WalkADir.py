# Morgan Wilkinson
# 07/21/2019

# This program walks a directory and its subfolders

import os

def walk(top):
    for folderName, subfolders, filenames in os.walk(top):
        print("The current folder is " +folderName)

        for subfolder in subfolders:
            print("SUBFOLDER OF " +folderName+ ": " +subfolder)

        for filename in filenames:
            print("FILE INSIDE " +folderName+ ": " +filename)

        print("")

walk("/Users/morgan/Desktop")
