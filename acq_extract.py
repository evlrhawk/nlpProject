# Imports
import os 
import pandas as pd
import sys
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
nltk.download('punkt')
from nltk.tokenize import blankline_tokenize
from nltk.tokenize import WhitespaceTokenizer
from nltk.tag import pos_tag
nltk.download('averaged_perceptron_tagger')


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
        tagged_sent = pos_tag(para.split())
        propernouns = [word for word,pos in tagged_sent if pos == 'NNP']

        print(propernouns)


        # print(para)
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





# # glove.6b.zip  bio tagging
# import spaCy
# import venv
# import nltk
# import word_tokenize
# import blankline_tokenize # seperations be /n line or pragraphs
# import bigrams, trigrams, ngrams
# from nltk.stem import PorterStemmer/LancasterStemmer/SnowballStemmer
# from nltk.stem import wordnet
# from nltk.stem import WordNetLemmaizer
# from nltk.corpus import stopwords
# import re
# sbst=SnowballStemmer('english')
# pst=PorterStemmer()
# # import nltk.corpus # just for using 
# # Some functions down here
# our_words = word_tokenize(sentence) 
# for word in our_words:
#     fdist[word.lower()]+=1 #frequency of words
# fdist
# fdist['<word wanted to be searched>']
# fdist.most_common(10)
# Sentence_bigrams = <list/set>(nltk.bigrams(sentence))
# Sentence_ngrams = <list/set>(nltk.ngrams(sentence, 5))
# # Stemming:
# pst.stem("having")


# #Lemmatization:

# punctuation = compile(r'[-.?!,:;()|0-9]')
# post_punctuation=[]
# for words in Sentence:
#     word = punctuation.sub("",words)
#     if len(word)>0:
#         post_punctuation.append(word)

# for token in sent_tokens:
#     print(nltk.pos_tag([token]))





