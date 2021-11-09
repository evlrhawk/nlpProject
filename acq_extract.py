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
    _acquired = "---"
    _acqbus = "---"
    _acqloc = "---"
    _dlramt = "---"
    _purchaser = "---"
    _seller = "---"
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

        #Do Stuff to get data needed

        #Get Sentence Breakdown
        storyText = open(path + file,"r")
        SENTENCES.append(sent_tokenize(storyText.read()))

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

        #print(propernouns)


        # print(para)
        #append story with data
        STORIES.append(story)

def writeData(docList:str):
    global STORIES

    fileName = docList[:-4] + ".templates"
    outFile = open(fileName, "w")
    
    for story in STORIES:
        print("TEXT:", story._text, file=outFile)
        print("ACQUIRED:", story._acquired, file=outFile)
        print("ACQBUS:", story._acqbus, file=outFile)
        print("ACQLOC:", story._acqloc, file=outFile)
        print("DLRAMT:", story._dlramt, file=outFile)
        print("PURCHASER:", story._purchaser, file=outFile)
        print("SELLER:", story._seller, file=outFile)
        print("STATUS:", story._status, file=outFile)

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

# Driver Section
if (len(sys.argv)) == 2:
    getFiles(sys.argv[1])
    readFiles()

    for story,sentence in zip(STORIES,SENTENCES):
        story._dlramt = "\"" + findPrice(sentence) + "\""
        if story._dlramt == "\"---\"":
            story._dlramt = "---"

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





