# Imports
import os
from nltk.tokenize.regexp import RegexpTokenizer 
import pandas as pd
import sys
import nltk
import spacy
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
from spacy.util import get_package_path
nltk.download('punkt')
from nltk.tokenize import blankline_tokenize
from nltk.tokenize import WhitespaceTokenizer
from nltk.tag import pos_tag
nltk.download('averaged_perceptron_tagger')
from nltk import ne_chunk
nltk.download('maxent_ne_chunker')
nltk.download('words')
from nltk.corpus import stopwords
# from nltk.probability import FreqDist   #Could be used to reduce our most frequent words like: "the, a, ',', '.', "
# fdist = FreqDist()
# fdist_top10 = fdist.most_common(10)
# import re
# punctuation = compile(r'[-.?!,:;()|0-9]')


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

        #Do Stuff to get data needed
        for line in open(path + file,"r"):
            type(line)
            line = line.strip()
            # sent_token = sent_tokenize(line)
            para_tokenize = blankline_tokenize(line)
            # line_tokenize = word_tokenize(line)
            if not para_tokenize:
                para = []
            if para_tokenize:
                para.extend(para_tokenize)
            # line_tokenize = word_tokenize(line)
            # if not line_tokenize:
            #     para = []
            # if line_tokenize:
            #     para.extend(line_tokenize)


            pass
        para = ' '.join(para)
        words_tagged = pos_tag(para.split())
        chunked_tagged = ne_chunk(words_tagged)
        # organizations = [word for word,pos in chunked_tagged if pos == 'NNP']
        # print(chunked_tagged)


        
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





