import os, sys
import json
from PIL import Image
import numpy as np
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from skimage.io import imread
import colorsys

TOLERANCE=2

def isHorizontal(w1,w2):
    b1=w1['TextBB']
    b2=w2['TextBB']
    #if abs(b2[1]-b1[1])<TOLERANCE and abs(b2[3]-b1[3])<TOLERANCE: print w1['Text'],w2['Text'];
    return abs(b2[1]-b1[1])<TOLERANCE and abs(b2[3]-b1[3])<TOLERANCE

'''
def show_img(img):
     width = img.shape[1]/75.0
     height = img.shape[0]*width/img.shape[1]
     f = plt.figure(figsize=(width, height))
     plt.imshow(img)
     pylab.show()
'''

#TODO: we are resorted to use HSV color scheme. These needs to be fixed
#asap.

def hsvColorExists(im):
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            rgbcolor=im[i][j]
            r=rgbcolor[0]
            g=rgbcolor[1]
            b=rgbcolor[2]
            h,s,v=colorsys.rgb_to_hsv(rgbcolor[0]/255.,rgbcolor[1]/255.,rgbcolor[2]/255.)
            h=int(360*h)
            s=int(100*s)
            v=int(100*v)
            #print (h,s,v)
            if v>5 and s>10:
                return True
    return False         
     
def imagePixelExists(w1,w2,imLoc):
    im=imread(imLoc)
    #thresh=threshold_otsu(im)
    #binary=im>thresh
 
    bbw1=w1['TextBB']
    bbw2=w2['TextBB']
    l=w1
    r=w2 
    if bbw1[0]>bbw2[0]:
        l=w2
        r=w1
    #im=Image.open(imLoc)
    #print im.size,np.array(im).shape,type(np.array(im))
    b=[round(x) for x in [l['TextBB'][2]+TOLERANCE,min(l['TextBB'][1],r['TextBB'][1]),\
    r['TextBB'][0]-TOLERANCE,max(l['TextBB'][3],r['TextBB'][3])]]

    if b[0]>=b[2]:
        #print "words\"",l['Text'],"\" and \"",r['Text'],"\" too close, should be merged"
        return False  
    if hsvColorExists((im[b[1]:b[3],b[0]:b[2]])):
        #print "pixel exists between",l['Text'],"and",r['Text'],b
        return True
    else:
        #print "pixel does not exist between",l['Text'],"and",r['Text'],b 
        return False 
 

def hDist(w1,w2):
    left=w1
    right=w2 
    if w1['TextBB'][0]>w2['TextBB'][0]:
        left=w2
        right=w1
    #if w1['Text']=="period": print right['TextBB'][0]-left['TextBB'][2]; 
    return max(0,right['TextBB'][0]-left['TextBB'][2]) 
 
def mergeScores(lw,lWs,imageLoc):
    mWList=[]
    for w in lWs:
        if not isHorizontal(lw,w):
            mWList.append((w,-1))
        elif lw['Rotation'] != w['Rotation']:
            mWList.append((w,-1))  
        elif imagePixelExists(lw,w,imageLoc):
            mWList.append((w,-1))
        else:
            mWList.append((w,hDist(lw,w))) 
    return mWList      

def removeWord(w,ws):
    return [x for x in ws if cmp(x,w)!=0]

def merge(w,pws):
    pws=sorted([x for x in pws if x[1]!=-1], key=lambda tup: tup[1])
    if len(pws)==0:
        return (None,None)
    tmw=pws[0][0]
    
    l=tmw
    r=w 
    if tmw['TextBB'][0]>w['TextBB'][0]:
        l=w
        r=tmw
       
    mw={
        'Text':l['Text']+" "+r['Text'],
        'Rotation':l['Rotation'],
        'TextBB': [l['TextBB'][0],min(l['TextBB'][1],r['TextBB'][1]),r['TextBB'][2],max(l['TextBB'][3],r['TextBB'][3])],
        'TextLabel': 'legendstring',
        'TextLabelConf':(l['TextLabelConf']+r['TextLabelConf'])/2     
    }

    return (mw,tmw)   
    
def combineLegend(jsonLoc,imageLoc):
    #lW=legend Word
    imBB=json.load(open(jsonLoc))['ImageBB']
    lWs=[x for x in json.load(open(jsonLoc))['ImageText'] if x['TextLabel']=='legend']
    #for x in lWs: print x['Text'];
    finalLegends=[]
    while len(lWs)>1:
        lW=lWs[0]
        lWs=lWs[1:]
        pWs=mergeScores(lW,lWs,imageLoc)
        mergedlW,mergeWord=merge(lW,pWs)

        if mergedlW is not None:
            lWs=removeWord(mergeWord,lWs)
            lWs.append(mergedlW)
            #print "merged",mergedlW['Text']#,mergedlW['TextBB'] 
            #print "merged, now number of words: ",len(lWs)
        else:
            lW['TextLabel']='legendstring'
            finalLegends.append(lW)
            
    for lW in lWs:
            finalLegends.append(lW)
    
    return finalLegends
          
def main():
    jsonLoc=sys.argv[1]
    imageLoc=sys.argv[2]
    lWs=combineLegend(jsonLoc,imageLoc)
    modJsonLoc=jsonLoc[:-5]+"-lc.json"
    js=json.load(open(jsonLoc)) 
    js['Legends']=lWs
    json.dump(js,open(modJsonLoc,"wb")) 

if __name__ == "__main__":
    main()   
             
          

