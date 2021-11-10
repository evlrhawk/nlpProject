# Imports
import os
from nltk.tokenize.regexp import RegexpTokenizer 
import pandas as pd
import sys
import nltk
import spacy
# python -m spacy download en_core_web_md

from spacy import displacy  # use to see what is each word in our sentence is corresponding to
nlp = spacy.load("en_core_web_md")
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
from spacy.util import get_package_path
from spacy.matcher import Matcher
nltk.download('punkt')
from nltk.tokenize import blankline_tokenize
from nltk.tokenize import WhitespaceTokenizer
from nltk.tag import pos_tag
nltk.download('averaged_perceptron_tagger')
from nltk import ne_chunk
nltk.download('maxent_ne_chunker')
nltk.download('words')
from nltk.corpus import stopwords
nltk.download('stop_words')

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
        para = []
        docs = []
        #Do Stuff to get data needed
        for line in open(path + file,"r"):
            type(line)
            line = line.strip()
            para_tokenize = blankline_tokenize(line)
            if not para_tokenize:   # Breaking up our paragraphs into a paragraph
                para = []
            if para_tokenize:
                para.extend(para_tokenize)
            pass
        para = ' '.join(para)
        doc = nlp(para)
        story._purchaser = findPurchaser(doc)
        story._acquired = findAcquired(doc)
        story._seller = findSeller(doc)


        break
        #append story with data
        STORIES.append(story)
    return docs


def findPurchaser(doc):
    purchasers = []
    matcher = Matcher(nlp.vocab)
    pattern = [{"POS": "PROPN", "OP": "+"}] 
    matcher.add ("PURCHASERS", [pattern], greedy = "LONGEST")
    matches = matcher(doc)
    matches.sort(key = lambda x: x[1])
    for match in matches:
        purchasers.append(doc[match[1]:match[2]])
    purchaser = purchasers[0]
    return purchaser

def findAcquired(doc):
    acquireds = []
    matcher = Matcher(nlp.vocab)
    pattern = [{"POS": "PROPN", "OP": "+"}] 
    matcher.add ("PURCHASERS", [pattern], greedy = "LONGEST")
    matches = matcher(doc)
    matches.sort(key = lambda x: x[1])
    for match in matches:
        acquireds.append(doc[match[1]:match[2]])
    if len(acquireds) > 2:
        acquired = (acquireds[1])     
    return acquired

def findSeller(doc):
    sellers = []
    matcher = Matcher(nlp.vocab)
    pattern = [{"POS": "PROPN", "OP": "+"}] 
    matcher.add ("PURCHASERS", [pattern], greedy = "LONGEST")
    matches = matcher(doc)
    matches.sort(key = lambda x: x[1])
    for match in matches:
        sellers.append(doc[match[1]:match[2]])
    if len(sellers) > 3:
        seller = (sellers[2])   
    else:
        seller = "..."  
    return seller


def writeData(docList:str):
    global STORIES

    fileName = docList[:-4] + ".templates"
    outFile = open(fileName, "w")
    
    for story in STORIES:
        print("TEXT: ", story._text, file=outFile)
        for organizations in story._acquired:
            print("ACQUIRED: ", organizations, file=outFile)
        print("ACQBUS: ", story._acqbus, file=outFile)
        print("ACQLOC: ", story._acqloc, file=outFile)
        print("DLRAMT: ", story._dlramt, file=outFile)
        for organizations in story._purchaser:
            print("PURCHASER: ", organizations, file=outFile)
        for organizations in story._seller:
            print("SELLER: ", organizations, file=outFile)
        print("STATUS: ", story._status, file=outFile)

        outFile.write("\n")




# Driver Section
if (len(sys.argv)) == 2:
    getFiles(sys.argv[1])
    readFiles()
    writeData(sys.argv[1])
    
else:
    print("Please include files in the command line")




