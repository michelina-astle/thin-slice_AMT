__author__ = 'mmadaio'

import os
from random import randint


"""
Renames the filenames within the same directory
    Adds random number to beginning of filename
Usage:
python rename.py
"""

rootdir =  "Slices"
#filenames = os.listdir(path)


for root, subFolders, files in os.walk(rootdir):
	#print root
	#print subFolders
	#print files
    for subfolder in subFolders:
    	
    	filepath = root + "\\" + subfolder + "\\"
    	print filepath
    	for filename in os.listdir(filepath):

    		print filename
	    	if '.mp4' in filename:
				pathAndFile = filepath + filename
				print pathAndFile
				os.rename(pathAndFile, filename.replace("P", "{0}_P".format(randint(0,75))))
				print filename