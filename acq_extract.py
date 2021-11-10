# Imports
import pandas as pd
import sys
import nltk
import spacy
import numpy as np
# python -m spacy download en_core_web_md
from nltk.tokenize.regexp import RegexpTokenizer 
from spacy import displacy  # use to see what is each word in our sentence is corresponding to
from nltk.tokenize import sent_tokenize, word_tokenize
from spacy.util import get_package_path
from spacy.matcher import Matcher
from nltk.tokenize import blankline_tokenize
from nltk.tokenize import WhitespaceTokenizer
from nltk.tag import pos_tag
from nltk import ne_chunk
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
from nltk.corpus import stopwords
#nltk.download('stop_words')

nlp = spacy.load("en_core_web_md")
NER = spacy.load("en_core_web_trf")

# Globals
CURRENCIES = {"francs", "dlr", "dlrs", "lire", "stg", "yen"}
CURRENCY_ORIGIN = {"Belgian", "Canadian", "U.S."}
CURRENCY_TYPE = {"cash"}
NUMBERS = {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"}
QUANTITIES = {"billion", "mln", "MLN"}
UNDISCLOSED = {"disclose", "disclosed","undisclosed"}
UNDISCLOSED_NEXT = {"amount", "of", "sum", "terms"}
UNDISCLOSED_PREV = {"a", "almost","not", "been"}

FILENAME = []
PATH = []
SENTENCES = []
STORIES = []

# Classes
class Story:
    _text = "---"
    _acquired = []
    _acqbus = "---"
    _acqloc = "---"
    _dlramt = "---"
    _purchaser = []
    _seller = []
    _status = "---"
    _sentences = []
    _content = ""

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
    global SENTENCES
    global STORIES

    for path,file in zip(PATH, FILENAME):
        story = Story(file)
        para = []
        docs = []
        #Do Stuff to get data needed

        #Get Sentence Breakdown
        storyText = open(path + file,"r")
        SENTENCES.append(sent_tokenize(storyText.read()))

        for line in open(path + file,"r"):
            type(line)
            line = line.strip()
            para_tokenize = blankline_tokenize(line)
            if not para_tokenize:   # Breaking up our paragraphs into a paragraph
                para = []
            if para_tokenize:
                para.extend(para_tokenize)
            
        para = ' '.join(para)
        doc = nlp(para)
        story._purchaser = findPurchaser(doc)
        story._acquired = findAcquired(doc)
        story._seller = findSeller(doc)

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
    if purchasers:
        purchaser = purchasers[0]
    else:
        purchaser = "---"    
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
    else:
        acquired = "---"
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
        seller = "---"  
    return seller


def writeData(docList:str):
    global STORIES

    fileName = docList[:-4] + ".templates"
    outFile = open(fileName, "w")
    
    for story in STORIES:
        print("TEXT: ", story._text, file=outFile)
        if str(story._acquired) == "---":
            print("ACQUIRED: ", story._acquired, file=outFile)    
        else:
            print("ACQUIRED: ", "\"" + str(story._acquired) + "\"", file=outFile)
        print("ACQBUS: ", story._acqbus, file=outFile)
        for locations in story._acqloc:
            print("ACQLOC:", locations, file=outFile)
        print("DLRAMT: ", story._dlramt, file=outFile)
        if str(story._acquired) == "---":
            print("ACQUIRED: ", story._purchaser, file=outFile)    
        else:
            print("PURCHASER: ", "\"" + str(story._purchaser) + "\"", file=outFile) 
        if str(story._acquired) == "---":
            print("ACQUIRED: ", story._seller, file=outFile)    
        else:
            print("SELLER: ", "---", file=outFile)
        print("STATUS: ", story._status, file=outFile)

        #"\"" + str(story._seller) + "\""

        outFile.write("\n")

def findPrice(sentenceList:list):
    global CURRENCIES
    global CURRENCY_ORIGIN
    global CURRENCY_TYPE
    global NUMBERS
    global QUANTITIES
    global UNDISCLOSED
    global UNDISCLOSED_NEXT
    global UNDISCLOSED_PREV

    newSentence = ""

    for sentence in sentenceList:
        idx = 0
        sent = word_tokenize(sentence)
        for word in sent:
            if word.isdigit():
                if sent[idx+1] and sent[idx+1] in QUANTITIES:
                    if sent[idx+2] and sent[idx+2] in CURRENCY_ORIGIN:
                        if sent[idx+3] and sent[idx+3] in CURRENCIES:  
                            if sent[idx+4] and sent[idx+4] in CURRENCY_TYPE:  
                                newSentence = sent[idx] + " " + sent[idx+1] + " " + sent[idx+2] + " " + sent[idx+3] + " " + sent[idx+4]
                                # NUM QUANT CurOr Cur CurTyp
                            else:
                                newSentence = sent[idx] + " " + sent[idx+1] + " " + sent[idx+2] + " " + sent[idx+3]
                                # NUM QUANT CurOr Cur 
                    elif sent[idx+2] and sent[idx+2] in CURRENCIES:
                        if sent[idx+3] and sent[idx+3] in CURRENCY_TYPE:  
                            newSentence = sent[idx] + " " + sent[idx+1] + " " + sent[idx+2] + " " + sent[idx+3]
                            # NUM QUANT Cur CurTyp
                        else:
                            newSentence = sent[idx] + " " + sent[idx+1] + " " + sent[idx+2]
                            # NUM QUANT Cur
                elif sent[idx+1] and sent[idx+1] in CURRENCY_ORIGIN:
                    if sent[idx+2] and sent[idx+2] in CURRENCIES:  
                        if sent[idx+3] and sent[idx+3] in CURRENCY_TYPE:  
                            newSentence = sent[idx] + " " + sent[idx+1] + " " + sent[idx+2] + " " + sent[idx+3]
                            # NUM CurOr Cur CurTyp
                        else:
                            newSentence = sent[idx] + " " + sent[idx+1] + " " + sent[idx+2]
                            # NUM CurOr Cur
                elif sent[idx+1] and sent[idx+1] in CURRENCIES:
                    if sent[idx+2] and sent[idx+2] in CURRENCY_TYPE:  
                        newSentence = sent[idx] + " " + sent[idx+1] + " " + sent[idx+2]
                        # NUM Cur CurTyp
                    else:
                        newSentence = sent[idx] + " " + sent[idx+1] 
                        # NUM Cur 
            elif word in NUMBERS:
                if sent[idx+1] and sent[idx+1] in QUANTITIES:
                    if sent[idx+2] and sent[idx+2] in CURRENCY_ORIGIN:
                        if sent[idx+3] and sent[idx+3] in CURRENCIES:  
                            if sent[idx+4] and sent[idx+4] in CURRENCY_TYPE:  
                                newSentence = sent[idx] + " " + sent[idx+1] + " " + sent[idx+2] + " " + sent[idx+3] + " " + sent[idx+4]
                                # NUM QUANT CurOr Cur CurTyp
                            else:
                                newSentence = sent[idx] + " " + sent[idx+1] + " " + sent[idx+2] + " " + sent[idx+3]
                                # NUM QUANT CurOr Cur 
                    elif sent[idx+2] and sent[idx+2] in CURRENCIES:
                        if sent[idx+3] and sent[idx+3] in CURRENCY_TYPE:  
                            newSentence = sent[idx] + " " + sent[idx+1] + " " + sent[idx+2] + " " + sent[idx+3]
                            # NUM QUANT Cur CurTyp
                        else:
                            newSentence = sent[idx] + " " + sent[idx+1] + " " + sent[idx+2]
                            # NUM QUANT Cur
                elif sent[idx+1] and sent[idx+1] in CURRENCY_ORIGIN:
                    if sent[idx+2] and sent[idx+2] in CURRENCIES:  
                        if sent[idx+3] and sent[idx+3] in CURRENCY_TYPE:  
                            newSentence = sent[idx] + " " + sent[idx+1] + " " + sent[idx+2] + " " + sent[idx+3]
                            # NUM CurOr Cur CurTyp
                        else:
                            newSentence = sent[idx] + " " + sent[idx+1] + " " + sent[idx+2]
                            # NUM CurOr Cur
                elif sent[idx+1] and sent[idx+1] in CURRENCIES:
                    if sent[idx+2] and sent[idx+2] in CURRENCY_TYPE:  
                        newSentence = sent[idx] + " " + sent[idx+1] + " " + sent[idx+2]
                        # NUM Cur CurTyp
                    else:
                        newSentence = sent[idx] + " " + sent[idx+1]
                        # NUM Cur
            elif word in UNDISCLOSED:
                if sent[idx-1] and sent[idx-1] in UNDISCLOSED_PREV:
                    if sent[idx+1] and sent[idx+1] in UNDISCLOSED_NEXT:
                        newSentence = sent[idx-1] + " " + sent[idx] + " " + sent[idx+1]
                    else:
                        newSentence = sent[idx-1] + " " + sent[idx]
                elif sent[idx+1] and sent[idx+1] in UNDISCLOSED_NEXT:
                    newSentence = sent[idx] + " " + sent[idx+1]
                else:
                    newSentence = word
            elif newSentence == "":
                newSentence = "---"
            idx += 1
    return newSentence

def findLoc(sentenceList:list):
    global NER

    acqLoc = []

    for sentence in sentenceList:
        doc = NER(sentence)
        
        for ent in doc.ents:
            if ent.label_ == "GPE":
                acqLoc.append("\"" + ent.text + "\"")

    if not acqLoc:
        acqLoc.append("---")
        
    return acqLoc




# Driver Section
if (len(sys.argv)) == 2:
    getFiles(sys.argv[1])
    readFiles()

    for story,sentence in zip(STORIES,SENTENCES):
        story._dlramt = "\"" + findPrice(sentence) + "\""
        if story._dlramt == "\"---\"":
            story._dlramt = "---"

    for story,sentence in zip(STORIES,SENTENCES):
        story._acqloc = findLoc(sentence) 

    writeData(sys.argv[1])
    
else:
    print("Please include files in the command line")




