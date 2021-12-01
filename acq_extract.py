# Imports
import os
from re import A
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
# nltk.download('punkt')
from nltk.tokenize import blankline_tokenize
from nltk.tokenize import WhitespaceTokenizer
from nltk.tag import pos_tag
# nltk.download('averaged_perceptron_tagger')
from nltk import ne_chunk
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
from nltk.corpus import stopwords
# nltk.download('stop_words')
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
        story._purchaser = findPurchaser(doc)
        story._acquired = findAcquired(doc)
        story._seller = findSeller(doc)
        story._acqloc = location(doc)
        # story._acqbus = findacqbus(doc)
        story._status = findStatus(doc)
        # story._dlramt = money(doc)
        #append story with data
        STORIES.append(story)
        # i = i+1
    return


def findPurchaser(doc):
    purchasers = []
    words_before_pur = ["by"]
    aquisition_lemmas = ["buy", "purchase", "acquire", "get", "obtain", "take", "secure", "gain", "procure", "trade", "tendered", "pay"]
    matcher = Matcher(nlp.vocab)
    pattern = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"LEMMA": {"NOT_IN": aquisition_lemmas}, "OP": "*"}, {"LEMMA": {"IN": aquisition_lemmas}}]
    pattern1 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"LEMMA": {"NOT_IN": aquisition_lemmas}, "OP": "*"}, {"LEMMA": {"IN": aquisition_lemmas}}]
    pattern2 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"LEMMA": {"NOT_IN": aquisition_lemmas}, "OP": "*"}, {"LEMMA": {"IN": aquisition_lemmas}}]
    pattern3 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"LEMMA": {"NOT_IN": aquisition_lemmas}, "OP": "*"}, {"LEMMA": {"IN": aquisition_lemmas}}]
    pattern4 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"LEMMA": {"NOT_IN": aquisition_lemmas}, "OP": "*"}, {"LEMMA": {"IN": aquisition_lemmas}}]
    pattern5 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"LEMMA": "say" }]
    pattern6 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ORTH": {"IN": words_before_pur}}, {"ENT_TYPE": "ORG", "OP": "+"}]
    matcher.add ("PURCHASER_SENT", [pattern, pattern1, pattern2, pattern3, pattern4, pattern5, pattern6], greedy = "LONGEST")
    matches = matcher(doc)
    matches.sort(key = lambda x: x[1])
    for match in matches:
        purchasers.append(doc[match[1]:match[2]])
    if purchasers:
        purchaser = purchasers[0]
    else:
        purchaser = "---"
    doc2 = nlp(str(purchaser)) 
    purchasers = []
    matcher = Matcher(nlp.vocab)
    pattern = [{"ENT_TYPE": "ORG", "OP": "+"}] 
    matcher.add ("PURCHASER", [pattern], greedy = "LONGEST")
    matches = matcher(doc2)
    matches.sort(key = lambda x: x[1])
    for match in matches:
        purchasers.append(doc2[match[1]:match[2]])
    if purchasers:
        purchaser = purchasers[0]   
    else:
        purchaser = "---" 
    # print (purchaser) 
    return purchaser

def findStatus(doc):
    statuses= []
    status_other_lemmas = ["finish", "end", "complete", "conclude", "terminate", "tender", "agreed", "acquired"]
    status_start_lemmas = ["seek", "agree", "reached", "came", "decide", "finalized","interested","tetiative"]
    status_end_lemmas = ["buy", "purchase", "acquire", "get", "obtain", "take", "secure", "gain", "procure", "trade", "agree"]
    matcher = Matcher(nlp.vocab)
    pattern = [ {"LEMMA": {"IN": status_start_lemmas}, "OP": "+"}, {"LEMMA": {"NOT_IN": status_end_lemmas}, "OP": "*"}, {"LEMMA": {"IN": status_end_lemmas}}]
    pattern1 = [ {"LEMMA": {"IN": status_other_lemmas}}]
    matcher.add ("STATUS", [pattern, pattern1], greedy = "LONGEST")
    matches = matcher(doc)
    matches.sort(key = lambda x: x[1])
    for match in matches:
        statuses.append(doc[match[1]:match[2]])
    if statuses:
        status = statuses[0]
    else:
        status = "---"
    return status

def findAcquired(doc):
    acquireds = []
    possible_inter_words = ["of", "in", "for" ]
    acquire = []
    start_acquire_words = ["stake"]
    aquisition_lemmas = ["sell","buy", "purchase", "acquire", "get", "obtain", "take", "secure", "gain", "procure", "trade", "bid"]
    matcher = Matcher(nlp.vocab)
    
    # pattern = [{"ENT_TYPE": "ORG", "OP": "+"}] 
    pattern2 = [{"LEMMA": {"IN": aquisition_lemmas}}, {"ORTH": {"IN": possible_inter_words}, "OP": "*"}, {"ENT_TYPE": "ORG", "OP": "+"}]
    pattern3 = [{"ORTH": {"IN": possible_inter_words}, "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "+"}]
    pattern4 = [{"ORTH": {"IN": start_acquire_words}}, {"ORTH": {"IN": possible_inter_words}, "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "+"}]
    pattern5 = [{"LEMMA": {"IN": aquisition_lemmas}}, {"ENT_TYPE": "ORG", "OP": "!"},{"ENT_TYPE": "ORG", "OP": "+"}]
    pattern6 = [{"LEMMA": {"IN": aquisition_lemmas}}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "+"}]
    pattern7 = [{"LEMMA": {"IN": aquisition_lemmas}}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "+"}]
    pattern8 = [{"LEMMA": {"IN": aquisition_lemmas}}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "+"}]
    pattern9 = [{"LEMMA": {"IN": aquisition_lemmas}}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "+"}]
    pattern10 = [{"LEMMA": {"IN": aquisition_lemmas}}, {"ENT_TYPE": "ORG", "OP": "+"}]
    pattern11 = [{"LEMMA": {"IN": aquisition_lemmas}}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "+"}]
    
    
    matcher.add ("ACQUIRED_SENT", [ pattern2, pattern3, pattern4, pattern5, pattern6, pattern7, pattern8, pattern9, pattern10, pattern11], greedy = "LONGEST")
    matches = matcher(doc)
    matches.sort(key = lambda x: x[1])
    for match in matches:
        acquireds.append(doc[match[1]:match[2]])
    if acquireds:
        acquired = (acquireds[0])     
    # if len(acquireds)>2:
    #     acquired = (acquireds[1])  
    else:
        acquired = "---"
    doc2 = nlp(str(acquired)) 
    acquireds = []
    matcher = Matcher(nlp.vocab)
    pattern = [{"ENT_TYPE": "ORG", "OP": "+"}] 
    matcher.add ("ACQUIRED", [pattern], greedy = "LONGEST")
    matches = matcher(doc2)
    matches.sort(key = lambda x: x[1])
    for match in matches:
        acquireds.append(doc2[match[1]:match[2]])
    if acquireds:
        acquired = acquireds[0]   
    else:
        acquired = "---" 

    return acquired

def findSeller(doc):
    sellers = []
    matcher = Matcher(nlp.vocab)
    sell_lemmas = ["offer", "sale", "transaction"]
    seller_list = ["sold", "sell", "tendered", "sells" ]
    past_seller = ["were", "was", "will", "would", "has", "had"]


    pattern = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ORTH": {"IN": seller_list}}]
    pattern1 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ORTH": {"NOT_IN": seller_list}, "OP": "*"}, {"ORTH": {"IN": seller_list}}]
    pattern2 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ORTH": {"IN": seller_list}}]
    pattern3 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ORTH": {"IN": seller_list}}]
    pattern4 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ORTH": {"IN": seller_list}}]
    pattern5 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ORTH": {"IN": seller_list}}]
    pattern6 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ORTH": {"IN": seller_list}}]
    pattern7 = [{"ORTH": "from" }, {"ENT_TYPE": "ORG", "OP": "+"} ]
    pattern8 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ORTH": {"IN": past_seller }}, {"ORTH": {"IN": seller_list}} ]
    pattern9 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"LEMMA": {"NOT_IN": sell_lemmas}, "OP": "*"}, {"LEMMA": {"IN": sell_lemmas}}]
    
    
    matcher.add ("SELLER_SENT", [pattern1, pattern2, pattern3, pattern4, pattern5, pattern6, pattern8, pattern7, pattern9], greedy = "LONGEST")
    matches = matcher(doc)
    matches.sort(key = lambda x: x[1])
    for match in matches:
        sellers.append(doc[match[1]:match[2]])
    if sellers:
        # print (sellers)
        seller = sellers[0]   
    else:
        seller = "---" 
    doc2 = nlp(str(seller)) 
    sellers = []
    matcher = Matcher(nlp.vocab)
    pattern = [{"ENT_TYPE": "ORG", "OP": "+"}] 
    matcher.add ("SELLER", [pattern], greedy = "LONGEST")
    matches = matcher(doc2)
    matches.sort(key = lambda x: x[1])
    for match in matches:
        sellers.append(doc2[match[1]:match[2]])
    if sellers:
        seller = sellers[0]   
    else:
        seller = "---" 
    return seller


def findacqbus(doc):
    sellers = []
    acqbus_lemmas = ["buy", "purchase", "acquire", "get", "obtain", "take", "secure", "gain", "procure", "trade", "tendered"]
    matcher = Matcher(nlp.vocab)
    acqbus_lemmas = ["engaged"]
    acqbus_words = ["its", "the", "a", "of", "and" ,"'s"]
    acqbus_end_words = ["to", "business", "company", "division", ".", "is", ","]
    acqbus_end_end_words = ["business", "company", "division"]
    acqbus_inter_words = ["provide"]


    # pattern7 = [{"ENT_TYPE": "ORG", "OP": "+"},{"ORTH": {"IN":  acqbus_inter_words}, "OP": "+"},  {"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"IN": acqbus_end_end_words}}]
    # pattern = [{"LEMMA": {"IN": acqbus_lemmas}, "OP": "+"}, {"ORTH": {"IN":  acqbus_words}, "OP": "*"}, {"ORTH": {"NOT_IN": acqbut_end_words}, "OP": "*"},{"ORTH": {"IN": acqbut_end_words}}]
    # pattern1 = [{"ORTH": {"IN":  acqbus_words}, "OP": "+"},{"ENT_TYPE": "LOC", "OP": "+"},  {"ORTH": {"NOT_IN": acqbut_end_words}, "OP": "*"},{"ORTH": {"IN": acqbut_end_words}}]
    # pattern = [{"ENT_TYPE": "ORG", "OP": "+"},{"ORTH": {"IN":  acqbus_words}, "OP": "+"},  {"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"IN": acqbus_end_end_words}}]
    # pattern1 = [{"ENT_TYPE": "ORG", "OP": "+"},{"ORTH": {"IN":  acqbus_words}, "OP": "+"},  {"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"IN": acqbus_end_end_words}}]
    # pattern2 = [{"ENT_TYPE": "ORG", "OP": "+"},{"ORTH": {"IN":  acqbus_words}, "OP": "+"},  {"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"NOT_IN": acqbus_end_words}}, {"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"IN": acqbus_end_end_words}}]
    # pattern3 = [{"ENT_TYPE": "ORG", "OP": "+"},{"ORTH": {"IN":  acqbus_words}, "OP": "+"},  {"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"IN": acqbus_end_end_words}}]
    # pattern4 = [{"ENT_TYPE": "ORG", "OP": "+"},{"ORTH": {"IN":  acqbus_words}, "OP": "+"},  {"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"IN": acqbus_end_end_words}}]
    # pattern5 = [{"ENT_TYPE": "ORG", "OP": "+"},{"ORTH": {"IN":  acqbus_words}, "OP": "+"},  {"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"IN": acqbus_end_end_words}}]
    # pattern6 = [{"ENT_TYPE": "ORG", "OP": "+"},{"ORTH": {"IN":  acqbus_words}, "OP": "+"},  {"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"NOT_IN": acqbus_end_words}},{"ORTH": {"IN": acqbus_end_end_words}}]

    # matcher.add ("ACQBUS_SENT", [pattern, pattern1, pattern2, pattern3, pattern4, pattern5, pattern6, pattern7], greedy = "LONGEST")
    matches = matcher(doc)
    matches.sort(key = lambda x: x[1])
    for match in matches:
        sellers.append(doc[match[1]:match[2]])
    if sellers:

        seller = sellers[0]   
    else:
        seller = "---" 
    # print (seller)
    doc2 = nlp(str(seller)) 
    sellers = []
    matcher = Matcher(nlp.vocab)


    pattern = [{"ORTH": {"NOT_IN":  acqbus_words}}, {"ORTH": {"NOT_IN": acqbus_end_end_words}, "OP": "*"}]
    # pattern1 = [{"ORTH": {"NOT_IN":  acqbus_words}, "OP": "?"},{"ENT_TYPE": "LOC", "OP": "!"},  {"ORTH": {"NOT_IN": acqbut_end_words}, "OP": "*"}]
    

    matcher.add ("ACQBUS", [pattern], greedy = "LONGEST")
    matches = matcher(doc2)
    matches.sort(key = lambda x: x[1])
    for match in matches:
        sellers.append(doc2[match[1]:match[2]])
    if sellers:
        seller = sellers[0]   
    else:
        seller = "---" 

    return seller



def location(doc):
    locations = []
    matcher = Matcher(nlp.vocab)

    pattern = [{"ENT_TYPE": "LOC", "OP": "+"}] 
    pattern2 = [{"ENT_TYPE": "GPE", "OP": "+"}] 
    matcher.add ("LOCATION_SENT", [ pattern, pattern2], greedy = "LONGEST")
    matches = matcher(doc)
    matches.sort(key = lambda x: x[1])
    for match in matches:
        locations.append(doc[match[1]:match[2]])
    if locations:

        place = locations[0]   
    else:
        place = "---" 
    return place

def money(doc):
    values = []
    matcher = Matcher(nlp.vocab)
    pattern = [{"ENT_TYPE": "MONEY", "OP": "+"}] 
    matcher.add ("LOCATION_SENT", [ pattern], greedy = "LONGEST")
    matches = matcher(doc)
    matches.sort(key = lambda x: x[1])
    for match in matches:
        values.append(doc[match[1]:match[2]])
    if values:
        money = values[0]   
    else:
        money = "---" 
    return money





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
        if str(story._acqbus) == "---":
            print("ACQBUS: ", story._acqbus, file=outFile)    
        else:
            print("ACQBUS: ", "\"" + str(story._acqbus) + "\"", file=outFile) 
        if str(story._acqloc) == "---":
            print("ACQLOC: ", story._acqloc, file=outFile)    
        else:
            print("ACQLOC: ", "\"" + str(story._acqloc) + "\"", file=outFile) 
        if str(story._dlramt) == "---":
            print("DLRAMT: ", story._dlramt, file=outFile)    
        else:
            print("DLRAMT: ", "\"" + str(story._dlramt) + "\"", file=outFile) 
        if str(story._purchaser) == "---":
            print("PURCHASER: ", story._purchaser, file=outFile)    
        else:
            print("PURCHASER: ", "\"" + str(story._purchaser) + "\"", file=outFile) 
        if str(story._seller) == "---":
            print("SELLER: ", story._seller, file=outFile)    
        else:
            print("SELLER: ", "\"" + str(story._seller) + "\"", file=outFile) 
        if str(story._status) == "---":
            print("STATUS: ", story._status, file=outFile)    
        else:
            print("STATUS: ", "\"" + str(story._status) + "\"", file=outFile) 
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
    readFiles_ans()
    readFiles()
    writeData(sys.argv[2])
    