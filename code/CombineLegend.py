import os, sys
import json
from PIL import Image
import numpy as np

TOLERANCE=2

def isHorizontal(w1,w2):
    b1=w1['TextBB']
    b2=w2['TextBB']
    return abs(b2[1]-b1[1])<TOLERANCE and abs(b2[3]-b1[3])<TOLERANCE

def imagePixelExists(w1,w2,imLoc):
    im=np.asarray(Image.open(imLoc)
      
def mergeScores(lw,lWs,imageLoc):
    mWList=[]
    for w in lWs:
        if not isHorizontal(lw,w):
            mWList.append((w,0))
        elif imagePixelExists(lw,w,imageLoc):
            mWList.append((w,0))
        else:
            mWList.append((w,hDist(lw,w))) 
    return mWList      
    
def combineLegend(jsonLoc,ImageLoc):
    #lW=legend Word
    lWs=[x for x in open(jsonLoc)['ImageText'] if x['TextLabel']=='legend']
    finalLegends=[]
    while len(lWs)>0:
        lW=lWs[0]
        lWs=lWs[1:]
        pWs=mergeScores(lW,removeWord(lW,lWs),ImageLoc)
        mergedlW,mergeWord=merge(lW,pWs)
        if mergedlW!=None:
            lWs=removeWord(mergeWord,lWs)
            lWs.append(mergedlW)
            print "merged, now number of words: ",len(lWs)
        else:
            finalLegends.append(lW)
    
    for lW in lWs:
            finalLegends.append(lW)
          
              
          

