# Imports
import pandas as pd
import sys
import nltk
import spacy
import numpy as np
# python -m spacy download en_core_web_md
from nltk.tokenize.regexp import RegexpTokenizer 
from spacy.tokens import DocBin
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
from thinc.types import Fal
from spacy.training import Corpus
#nltk.download('stop_words')

#nlp = spacy.load("en_core_web_md")
nlp = spacy.load("en_core_web_trf")

# Globals
CURRENCIES = {"francs", "dlr", "dlrs", "lire", "pesos", "stg", "yen"}
CURRENCY_ORIGIN = {"Belgian", "Canadian", "N.Z", "U.S."}
CURRENCY_TYPE = {"cash"}
KILL_WORDS = {"sales", "prices", "profits", "share", "more than", "not less than", "opposed"}#, "shares", "bid"}
NUMBERS = {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"}
QUANTITIES = {"billion", "Billion", "bln", "BLN", "million", "Million", "mln", "MLN"}
UNDISCLOSED = {"disclose", "disclosed","undisclosed"}
UNDISCLOSED_NEXT = {"amount", "of", "sum"} #, "terms"}
UNDISCLOSED_PREV = {"a", "almost","not", "been"}

FILENAME = []
PATH = []
SENTENCES = []
STORIES = []
FILENAME_ans = []
PATH_ans = []
STORIES_ans = []
ans_list_list = []
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
def isNumber(n:str):
    if n.isdigit() or n.replace(".", "").isdigit():
        return True
    return False

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
    global ans_list_list
    i = 0
    
    for path,file in zip(PATH, FILENAME):
        story = Story(file)
        para = []
        docs = []
        #Do Stuff to get data needed

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
        story._acqbus = findacqbus(doc)
        story._status = findStatus(doc)
        #append story with data
        STORIES.append(story)
        # i = i+1
    return

def findPurchaser(doc):
    purchasers = []
    aquisition_lemmas = ["buy", "purchase", "acquire", "get", "obtain", "take", "secure", "gain", "procure", "trade"]
    matcher = Matcher(nlp.vocab)
    pattern = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"LEMMA": {"NOT_IN": aquisition_lemmas}, "OP": "*"}, {"LEMMA": {"IN": aquisition_lemmas}}]
    pattern1 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"LEMMA": {"NOT_IN": aquisition_lemmas}, "OP": "*"}, {"LEMMA": {"IN": aquisition_lemmas}}]
    pattern2 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"LEMMA": {"NOT_IN": aquisition_lemmas}, "OP": "*"}, {"LEMMA": {"IN": aquisition_lemmas}}]
    pattern3 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"LEMMA": {"NOT_IN": aquisition_lemmas}, "OP": "*"}, {"LEMMA": {"IN": aquisition_lemmas}}]
    pattern4 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"LEMMA": {"NOT_IN": aquisition_lemmas}, "OP": "*"}, {"LEMMA": {"IN": aquisition_lemmas}}]
    # pattern1 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"LEMMA": {"IN": aquisition_lemmas}}]    
    # pattern2 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"LEMMA": {"IN": aquisition_lemmas}}]
    # pattern3 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"LEMMA": {"IN": aquisition_lemmas}}]
    # pattern4 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"LEMMA": {"IN": aquisition_lemmas}}]
    # pattern5 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"LEMMA": {"IN": aquisition_lemmas}}]
    # pattern6 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"LEMMA": {"IN": aquisition_lemmas}}]
    pattern5 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ORTH": "said" }]
    matcher.add ("PURCHASER_SENT", [pattern5, pattern, pattern4, pattern1, pattern2, pattern3], greedy = "LONGEST")
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
    status_other_lemmas = ["finish", "end", "complete", "conclude", "terminate"]
    status_start_lemmas = ["seek", "agree", "reached", "came", "decide"]
    status_end_lemmas = ["buy", "purchase", "acquire", "get", "obtain", "take", "secure", "gain", "procure", "trade", "agree"]
    matcher = Matcher(nlp.vocab)
    pattern = [ {"LEMMA": {"IN": status_start_lemmas}, "OP": "+"}, {"LEMMA": {"NOT_IN": status_end_lemmas}, "OP": "*"}, {"LEMMA": {"IN": status_end_lemmas}}]
    pattern = [ {"LEMMA": {"IN": status_other_lemmas}}]
    matcher.add ("STATUS", [pattern], greedy = "LONGEST")
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
    acquire = []
    matcher = Matcher(nlp.vocab)
    pattern = [{"ENT_TYPE": "ORG", "OP": "+"}] 
    # pattern = [{"LEMMA": {"IN": ["sale", "buy", "purchase", "acquire", "get", "obtain", "take", "secure", "gain", "procure", "trade"]}}]
    # pattern = [{"ENT_TYPE": "ORG"}]
    # pattern = [{{"POS": "PROPN", "OP": "+"}, {"-"}, {"POS": "PROPN", "OP": "+"}}]
    matcher.add ("ACQUIRED_SENT", [pattern], greedy = "LONGEST")
    matches = matcher(doc)
    matches.sort(key = lambda x: x[1])
    for match in matches:
        acquireds.append(doc[match[1]:match[2]])
    if len(acquireds) > 2:
        acquired = (acquireds[1])     
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
    pattern7 = [{"ORTH": "from" }, {"ENT_TYPE": "ORG", "OP": "+"} ]
    pattern1 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ORTH": {"IN": ["sold", "sell", "sells"]}}]
    pattern2 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ORTH": {"IN": ["sold", "sell", "sells"]}}]
    pattern3 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ORTH": {"IN": ["sold", "sell", "sells"]}}]
    pattern4 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ORTH": {"IN": ["sold", "sell", "sells"]}}]
    pattern5 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ORTH": {"IN": ["sold", "sell", "sells"]}}]
    pattern6 = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ORTH": {"IN": ["sold", "sell", "sells"]}}]
    pattern = [{"ENT_TYPE": "ORG", "OP": "+"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"ENT_TYPE": "ORG", "OP": "!"}, {"LEMMA": {"NOT_IN": sell_lemmas}, "OP": "*"}, {"LEMMA": {"IN": sell_lemmas}}]
    matcher.add ("SELLER_SENT", [ pattern7, pattern1, pattern2, pattern3, pattern4, pattern5, pattern6, pattern], greedy = "LONGEST")
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
    matcher = Matcher(nlp.vocab)
    acqbus_lemmas = ["engaged"]

    prev = ["provide", "provides", "give", "gives"]
    post = ["to", "for"]
    pattern = [{"ORTH": {"IN": prev}}, {"ORTH": {"NOT_IN": post}, "OP": "*"}]
    #pattern1 = [{"POS": "ADJ"}, {"ORTH": {"NOT_IN": ["business"]}, "OP": "*"}]
    matcher.add ("BUS_ACQ", [ pattern], greedy = "LONGEST")
    matches = matcher(doc)
    matches.sort(key = lambda x: x[1])
    for match in matches:
        sellers.append(doc[match[1]:match[2]])
    if sellers:
        print (sellers)
        seller = sellers[0]   
    else:
        seller = "---" 
    doc2 = nlp(str(seller)) 
    sellers = []
    matcher = Matcher(nlp.vocab)
    pattern = [{"ORTH": {"NOT_IN": prev}, "OP": "*"}]
    #pattern1 = [{"POS": "NOUN", "OP": "*"}] 
    matcher.add ("BUS", [pattern], greedy = "LONGEST")
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
        # print (sellers)
        place = locations[0]   
    else:
        place = "---" 
    # doc2 = nlp(str(seller)) 
    # sellers = []
    # matcher = Matcher(nlp.vocab)
    # pattern = [{"ENT_TYPE": "ORG", "OP": "+"}] 
    # matcher.add ("SELLER", [pattern], greedy = "LONGEST")
    # matches = matcher(doc2)
    # matches.sort(key = lambda x: x[1])
    # for match in matches:
    #     sellers.append(doc2[match[1]:match[2]])
    # if sellers:
    #     seller = sellers[0]   
    # else:
    #     seller = "---" 
    return place

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
        
        print("DLRAMT: ", story._dlramt, file=outFile)
        
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

def findPrice(sentenceList:list):
    global CURRENCIES
    global CURRENCY_ORIGIN
    global CURRENCY_TYPE
    global KILL_WORDS
    global NUMBERS
    global QUANTITIES
    global UNDISCLOSED
    global UNDISCLOSED_NEXT
    global UNDISCLOSED_PREV

    newSentence = ""

    for sentence in sentenceList:
        idx = 0
        sent = word_tokenize(sentence)
        kill = any(item in KILL_WORDS for item in sent)
        
        if not kill:
            for word in sent:
                if isNumber(word):
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
    locations = []

    sent = str(sentenceList)
    newSent = sent_tokenize(sent)

    for sentence in sentenceList:
        doc = nlp(sentence)
        found = False
        skip = False 
        location = ""

        for ent in doc.ents:
            if skip:
                skip = False
            elif ent.label_ == "GPE":
                location = "\"" + ent.text + "\""
                #skip = True
            # elif ent.label_ == "GPE":
            #     location = "\"" + ent.text + "\"" 
            if location not in locations:
                locations.append(location)

    acqLoc.clear()
    #Filter list of possible locations
    _skip = False
    for loc in locations:
        #print (loc)
        if _skip:
            _skip = False
        else:
            for sentence in newSent:
                sentence = sentence.replace("\\n", " ")
                idx = 0
                # if loc.strip() in sentence.strip():
                #print(loc, "\n")
                words = word_tokenize(sentence)
                for word in words:
                    num_words = loc.split()
                    #print(num_words, "\n")
                    if len(num_words) == 1:
                        if word in loc:
                            # if idx >= 1:    
                            #     if "of" in words[idx-1]:
                            #         found = True
                            #         pass # We dont want this one
                            if idx < len(num_words):
                                if "," in words[idx+1]:
                                    data = word + ", " + words[idx+2]
                                    data = data.replace("\\n", " ")
                                    data = data.replace("\\", " ")
                                    acqLoc.append(data)
                                    _skip = True
                                    found = True
                    idx += 1
                    if found:
                        break
                if found:
                    break
        if not found:
            acqLoc.append(loc)
        else: 
            found = False

    if len(acqLoc) > 1:
        return acqLoc[1:]
    elif acqLoc[0] == "":
        return ["---"]
    else:
        return acqLoc


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
if (len(sys.argv)) == 2:
    getFiles(sys.argv[1])
    readFiles()

    for story,sentence in zip(STORIES,SENTENCES):
        story._dlramt = "\"" + findPrice(sentence) + "\""
        if story._dlramt == "\"---\"":
            story._dlramt = "---"

    # for story,sentence in zip(STORIES,SENTENCES):
    #     story._acqloc = findLoc(sentence) 
    #     print(story._acqloc)

    writeData(sys.argv[1])
    
else:
    print("Please include files in the command line")


# Driver Section
# if (len(sys.argv)) == 3:
#     getFiles_ans(sys.argv[1])
#     getFiles(sys.argv[2])
#     readFiles_ans()
#     readFiles()
#     writeData(sys.argv[2])
    