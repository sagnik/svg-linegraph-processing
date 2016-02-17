import os, sys
import json

def mergeScores(lw,lWs,imageLoc):
    mWList=[]
    for w in lWs:
        if notHorizontal(lw,w):
            mWList.append((w,0))
        elif imagePixelExists(lw,w,imageLoc):
            mWList.append((w,0))
        else:
            mWList.append((w,hDist(lw,w))) 
    return mWList      
    
def combineLegend(jsonLoc,ImageLoc):
    #lW=legend Word
    lWs=[x for x in open(jsonLoc)['ImageText'] if x['TextLabel']=='legend']
    i=0
    while i<len(lWs):
        lW=lWs[i]
        print"checking word",i,"out of",len(lWs),"words"
        i+=1
        pWs=mergeScores(lW,list(set(lWs)-set([lW])),ImageLoc)
        mergedlW=merge(lW,pWs)
        if mergedlW!=None:
            lWs.append(mergedlW)
        
              
          

