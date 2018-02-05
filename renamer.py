__author__ = 'mmadaio'


import os, math

"""
Renames the filenames within the same directory
    Adds random number to beginning of filename
Usage:
python rename.py
"""

rootdir =  "Slice_Folder"
filenames = os.listdir(path)


for root, subFolders, files in os.walk(rootdir):
        if '.mp4' in files:
            os.rename(filename, filename.replace("P", "{0}_P".format(math.random())))
