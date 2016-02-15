from __future__ import division
import json
import sys
import numpy as np
from rtree import index as RTreeIndex
from collections import Counter
import re


classDict={
   'xaxislabel':1, 
   'xaxisvalue':2, 
   'yaxislabel':3,
   'yaxisvalue':4,
   'legend':5,
   'figurelabel':6, 
   'notclassified':7, 
   'undefined':7,
   
}

rtreeidx=None
SF=2 #scaling factor, see readme

def getRotation(word):
    return word['Rotation']

def distanceRatio(word,W,H):
    return [(word['TextBB'][0])/W,(W-word['TextBB'][2])/W,word['TextBB'][1]/H,(H-word['TextBB'][3])/H]  

def charRatio(word): #TODO: possible empty word?
    d=Counter([charType(x) for x in list(word)])
    return [d.get(x,0)/len(word) for x in [0,1,2]]

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_char(c):
    if re.search(r'[a-zA-z]',c) is not None:
        return True
    else:
        return False
  
def charType(c):
    if is_number(c):
        return 0
    elif is_char(c):
        return 1
    else:
        return 2  

def getWords(thisWordIndex,extendedLoc):
    return [x for x in list(rtreeidx.intersection(extendedLoc)) if x!=thisWordIndex] 
 

def FeatureExtractOneFile(loc):
    js=json.load(open(loc))
    if len(js['ImageText'])==0: 
        return None
    else:
        feat=[]
        #putting words in rtree
        global rtreeidx
        rtreeidx=RTreeIndex.Index()
 
        imgBB=js['ImageBB']
        W=SF*(imgBB[2]-imgBB[0])
	H=SF*(imgBB[3]-imgBB[1])
        
        for ind,imagetext in enumerate(js['ImageText']):
		rtreeidx.insert(ind,tuple(imagetext['TextBB']))

        for wordIndex,word in enumerate(js['ImageText']):
            featWord=[]
            wBB=word['TextBB']
            featWord.append(getRotation(word))
            for x in distanceRatio(word,W,H): 
                featWord.append(x)
            for x in charRatio(word['Text']):
                featWord.append(x) 
            featWord.append(float(is_number(word['Text'])))
            #number of words horizontally to the left to the end of the image, for Y axis label
            featWord.append(len(getWords(wordIndex,tuple([0,wBB[1]-10,wBB[0],wBB[1]+10]))))
            #number of words horizontally along the whole image, how many of them are numbers? for X value
            featWord.append(len(getWords(wordIndex,tuple([0,wBB[1]-10,W,wBB[1]+10]))))
            featWord.append(sum([int(is_number(js['ImageText'][x]['Text'])) for x in getWords(wordIndex,tuple([0,wBB[1]-10,W,wBB[1]+10]))]))
            #number of words above the word vertically, for figure label
            featWord.append(len(getWords(wordIndex,tuple([wBB[0]-10,0,wBB[2]+10,wBB[1]]))))
            #number of words below the word vertically, for X axis label
            featWord.append(len(getWords(wordIndex,tuple([wBB[0]-10,wBB[3],wBB[2]+10,H]))))
            #number of words within a larger rectangle of the word, how many of them are not numbers? for legend region
            featWord.append(len(getWords(wordIndex,tuple([wBB[0]-50,wBB[1]-50,wBB[2]+50,wBB[3]+50]))))
            featWord.append(sum([int(not is_number(js['ImageText'][x]['Text'])) for x in getWords(wordIndex,tuple([wBB[0]-50,wBB[1]-50,wBB[2]+50,wBB[3]+50]))]))
            #other features 

            #class label 
            #featWord.append(classDict[word['TextLabelGold']])
            feat.append(featWord) 
        print loc,len(js['ImageText']),np.array(feat).shape
        return feat

def main():
    jsonLoc=sys.argv[1]
    feat=np.array(FeatureExtractOneFile(jsonLoc))
    print feat.shape

if __name__=="__main__":
    main()
       
