# Morgan Wilkinson
# 07/21/2019

# This module deletes files with the specfied extentions

import os, send2trash

# Set directory
os.chdir('/Users/morgan/Desktop')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# This method irreveribly deletes the files
def totalDelete():
    for filename in os.listdir():
        if filename.endswith('.rtf'):
            print(filename)
            #os.unlink(filename)

#totalDelete()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#        
# This method sends the files to the trashbin where you can retrieve them if needed.
def safeDelete():
    baconFile = open('bacon.txt', 'a') # creates file
    baconFile.write('Bacon is nice to eat.')
    baconFile.close()

    send2trash.send2trash('bacon.txt')

#safeDelete()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#    
# This method is the more generalized form for multiple files of the same type.
def deleteFiles(fileType):
    for filename in os.listdir():
        if filename.endswith(fileType):
            print(filename)
            send2trash.send2trash(filename)

deleteFiles('.pdf')
