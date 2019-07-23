# Morgan Wilkinson
# 07/21/2019

# This module works with files to do a variety of functions.

# imports the shutil module which has functions to copy, move, rename and delete files.
# imports the os module to has access to the operating system 
import shutil, os

# This prints the current directory
print(os.getcwd())

# This returns a list of all the files in this directory
os.listdir('/Users/morgan/Desktop')

# This sets the current directory to the Desktop on a Mac
os.chdir('/Users/morgan/Desktop')

# This copys a file to a folder in the form (source, desktination).
# Instead of a folder as the destination you can add a file extention to copy the source to that file format.
shutil.copy('COMPLETE_IOS_12_DEVELOPMENT_GUIDE.pdf', 'Test')

# This copys an entire folder tree and its contents.
shutil.copytree('CS Foundation', 'Test')

# This moves an entire folder tree and its contents.
shutil.move('Test','/Users/morgan/Documents')

# This deletes a file at the specfied path
os.unlink('Untitled.rtf')

# This deletes an EMPTY folder at the specfied path
os.rmdir('Nine')

# This deletes a folder and its files
shutil.rmtree('Move')
