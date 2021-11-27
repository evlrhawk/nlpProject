# Imports
import os
from nltk.tokenize.regexp import RegexpTokenizer 
import pandas as pd
import sys
import nltk
import spacy
# python -m spacy download en_core_web_md
from spacy.tokens import DocBin
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
from spacy.training import Corpus

# Globals
FILENAME = []
PATH = []
STORIES = []
FILENAME_ans = []
PATH_ans = []
STORIES_ans = []
ans_list_list = []
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
    global ans_list_list
    i = 0
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
        

        # #MACHINE LEARNING
        # nlp = spacy.blank("en")
        # # ner = nlp.create_pipe("ner")
        # # nlp.add_pipe("ner", last=True)
        # # ner = nlp.get_pipe("ner")
        # if i <= 5:
        #     j = 0
        #     while j < 7:
        #         ent_list = ["ACQUIRED", "ACQBUS", "ACQLOC", "DLRAMT", "PURCHASER", "SELLER", "STATUS"]
        #         TRAIN_DATA = [(para, {"entities": [str(ans_list_list[i][j]), str(ent_list[j])]}),]
        #         db = DocBin()
        #         for text, annotations in TRAIN_DATA:
        #             # ner.add_label(annotations[2])
        #         # return nlp
        #             doc = nlp.make_doc(text)
        #             # ents = []
        #             # span = (annotations[0],annotations[1])
        #             # ents.append(annotations)
        #             # for word, label in annotations["entities"]:
        #             #     span = 
        #             #     ents.append(span)
        #             # print (annotations)
        #             # doc.ents = annotations
        #             db.add(doc)
        #         db.to_disk("./train.spacy")  
        #         j = j +1


        # # doc = nlp(para)
        # # if i > 5:
        # #     for ent in doc:
        # #         print(ent.text, ent.label_)  # what label corresponds to the text
        # #         pass




    #PATTERNS

        doc = nlp(para)
        # story._purchaser = findPurchaser(doc)
        story._acquired = findAcquired(doc)
        # story._seller = findSeller(doc)


        #append story with data
        STORIES.append(story)
        # i = i+1
    return


def findPurchaser(doc):
    purchasers = []
    aquisition_lemmas = ["sale", "buy", "purchase", "acquire", "get", "obtain", "take", "secure", "gain", "procure", "trade"]
    purchase = []
    matcher = Matcher(nlp.vocab)
    pattern = [{"POS": "PROPN", "OP": "+"}] 
    # pattern = [{"POS": "PROPN", "OP": "+"}, ]
    matcher.add ("PURCHASERS", [pattern], greedy = "LONGEST")
    matches = matcher(doc)
    matches.sort(key = lambda x: x[1])
    for match in matches:
        purchasers.append(doc[match[1]:match[2]])
    print (purchasers[0])
    purchaser = purchasers[0]

    return purchaser



def findAcquired(doc):
    acquireds = []
    acquire = []
    matcher = Matcher(nlp.vocab)
    pattern = [{"POS": "PROPN", "OP": "+"}] 
    # pattern = [{"LEMMA": {"IN": ["sale", "buy", "purchase", "acquire", "get", "obtain", "take", "secure", "gain", "procure", "trade"]}}]
    # pattern = [{"ENT_TYPE": "ORG"}]
    # pattern = [{{"POS": "PROPN", "OP": "+"}, {"-"}, {"POS": "PROPN", "OP": "+"}}]
    matcher.add ("PURCHASERS", [pattern], greedy = "LONGEST")
    matches = matcher(doc)
    matches.sort(key = lambda x: x[1])
    for match in matches:
        acquireds.append(doc[match[1]:match[2]])
    if len(acquireds) > 2:
        acquired = (acquireds[1])     
        print(acquired)
    return acquired

def findSeller(doc):
    sellers = []
    matcher = Matcher(nlp.vocab)
    pattern = [{"POS": "PROPN", "OP": "+"}] 
    # pattern = [{"LEMMA": {"IN": ["sale", "buy", "purchase", "acquire", "get", "obtain", "take", "secure", "gain", "procure", "trade"]}}]
    # pattern = [{"ENT_TYPE": "ORG"}]
    # pattern = [{{"POS": "PROPN", "OP": "+"}, {"-"}, {"POS": "PROPN", "OP": "+"}}]
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
        # print("TEXT: ", story._text, file=outFile)
        # print("ACQUIRED: ", story._acquired)
        # print("ACQBUS: ", story._acqbus, file=outFile)
        # print("ACQLOC: ", story._acqloc, file=outFile)
        # print("DLRAMT: ", story._dlramt, file=outFile)
        # print("PURCHASER: ", story._purchaser)
        # print("SELLER: ", story._seller)
        # print("STATUS: ", story._status, file=outFile)

        outFile.write("\n")



## Test and Train
def getFiles_ans(anslist:str):
    global FILENAME_ans
    global PATH_ans
    for line in open(anslist, "r"):
        newLine = line.strip()
        path_ans, file_ans = newLine.rsplit("/",1)
        path_ans += "/"
        PATH_ans.append(path_ans)
        FILENAME_ans.append(file_ans)

def readFiles_ans():
    global FILENAME_ans
    global PATH_ans
    global STORIES_ans
    global ans_list_list
 
    for path_ans,file_ans in zip(PATH_ans, FILENAME_ans):
        story_ans = Story(file_ans)
        para_ans = []
        docs_ans = []

        first = []
        i = 0
        ans_list = []
        for line in open(path_ans + file_ans,"r"):

            line = str(line.strip())
            first = line.split()
            first = first[1:]
            first = ' '.join(first)
            if i > 0:
                if first:
                    first = first.replace('"','')
                    ans_list.append(first)
            i = i+1
        
        ans_list_list.append(ans_list)





# Driver Section
if (len(sys.argv)) == 3:
    getFiles_ans(sys.argv[1])
    getFiles(sys.argv[2])
    # readFiles_ans()
    readFiles()
    writeData(sys.argv[2])
    