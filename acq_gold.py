# Imports
import os 
import pandas as pd
import sys

# Globals
FILENAME = []
PATH = []
STORIES = []

# Classes
class Story:
    _text = "---"
    _acquired = "---"
    _acqbus = "---"
    _acqloc = "---"
    _dlramt = "---"
    _purchaser = "---"
    _seller = "---"
    _status = "---"

    def __init__(self, text, acquired, acqbus, acqloc, dlramt, purchaser, seller, status):
        self._text = text
        self._acquired = acquired
        self._acqbus = acqbus
        self._acqloc = acqloc
        self._dlramt = dlramt
        self._purchaser = purchaser
        self._seller = seller
        self._status = status

# Methods
def getFiles(docList:str):
    global FILENAME
    global PATH

    for line in open(docList, "r"):
        newLine = line.strip()
        path, file = newLine.rsplit("/",1)
        path += "/"
        PATH.append(path)
        FILENAME.append(file)

def readFiles(docList:str):
    global FILENAME
    global PATH
    global STORIES

    fileName = docList[:-4] + ".templates"
    outFile = open(fileName, "w")

    for path,file in zip(PATH, FILENAME):
        #Do Stuff to get data needed
        for line in open(path + file,"r"):
            print(line.strip(), file=outFile)

getFiles(sys.argv[1])
readFiles(sys.argv[1])
