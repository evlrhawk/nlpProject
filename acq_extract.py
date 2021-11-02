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

    def __init__(self, text):#, acquired, acqbus, acqloc, dlramt, purhcaser, seller, status):
        self._text = text
        # self._acquired = acquired
        # self._acqbus = acqbus
        # self._acqloc = acqloc
        # self._dlramt = dlramt
        # self._purchaser = purchaser
        # self._seller = seller
        # self._status = status

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

def readFiles():
    global FILENAME
    global PATH
    global STORIES

    for path,file in zip(PATH, FILENAME):
        story = Story(file)

        #Do Stuff to get data needed
        for line in open(path + file,"r"):
            pass

        #append story with data
        STORIES.append(story)

def writeData(docList:str):
    global STORIES

    fileName = docList[:-4] + ".templates"
    outFile = open(fileName, "w")
    
    for story in STORIES:
        print("TEXT: ", story._text, file=outFile)
        print("ACQUIRED: ", story._acquired, file=outFile)
        print("ACQBUS: ", story._acqbus, file=outFile)
        print("ACQLOC: ", story._acqloc, file=outFile)
        print("DLRAMT: ", story._dlramt, file=outFile)
        print("PURCHASER: ", story._purchaser, file=outFile)
        print("SELLER: ", story._seller, file=outFile)
        print("STATUS: ", story._status, file=outFile)

        outFile.write("\n")


# Driver Section
if (len(sys.argv)) == 2:
    getFiles(sys.argv[1])
    readFiles()
    writeData(sys.argv[1])
    
else:
    print("Please include files in the command line")
