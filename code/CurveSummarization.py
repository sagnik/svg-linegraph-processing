from __future__ import division
import sys
import os
from skimage.io import imread
from skimage.color import rgb2hsv
from CurveSeperation import separateCurves
import xml.etree.cElementTree as ET
import numpy as np
import rsvg
import cairo
from PIL import Image
import json
from functools import reduce
from CurveLegendAssociation import show_img 
import random

def createCurves(svgLoc):
    separateCurves(svgLoc)

def getPointsSingleCurve(svgLoc,curveNumber):
    imgLoc=svgLoc[:-4]+"/"+os.path.split(svgLoc)[-1][:-4]+"-Curve-"+str(curveNumber)+".png"
    img=rgb2hsv(imread(imgLoc))
    return np.where(np.logical_and(np.greater_equal(img[:,:,1],0.06),np.greater_equal(img[:,:,2],0.1))) 

def createPng(svgLoc,W,H):
    img = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(W),int(H))
    ctx = cairo.Context(img)
    handle= rsvg.Handle(None, str(open(svgLoc).read()))
    handle.render_cairo(ctx)
    img.write_to_png(svgLoc[:-4]+".png")
    png = Image.open(svgLoc[:-4]+".png")
    png.load() # required for png.split()

    nonalphaPng = Image.new("RGB", png.size, (255, 255, 255))
    nonalphaPng.paste(png, mask=png.split()[3])
    nonalphaPng.save(svgLoc[:-4]+".png")

#TODO remove points that can belong to the legend region.
def notLegend(p,pp):
    sp=sorted(pp, key=lambda tup: tup[1])
    loc=sp.index(p)
    if loc==0 or loc==len(sp)-1 or loc==len(sp)-2: 
        return True;
    else:
        return not (sp[loc-1][1]==sp[loc][1] and sp[loc][1]==sp[loc+1][1]) #three consecutive points have same y value
        

def getCommonCurvePoints(curvePointsDict):
    curvexs=[np.unique(curvePointsDict[k][0][1]) for k in curvePointsDict]
    commonCurvexs=[]
    if len(curvexs)==1:
        commonCurvexs=curvexs[0] 
    commonCurvexs=reduce(np.intersect1d,(x for x in curvexs))
    commonCurvePoints=[] 
    sufficientCommonXpoints=False        
    if len(commonCurvexs)>30:
        print "sufficient common x points found for all curves" 
        sufficientCommonXpoints=True
    else:
        print "we couldn't find sufficient common x points for all curves, treating each curve separately" 
               
    for curvex,k in zip(curvexs,curvePointsDict.keys()):
        c=[]
        if sufficientCommonXpoints:
            c=[np.where((curvex==x))[0][0] for x in commonCurvexs]
        else:
           c=range(len(curvex))
        possiblePoints=[(curvePointsDict[k][0][1][i],curvePointsDict[k][0][0][i]) for i in c] 
        #points=[p for p in possiblePoints if notLegend(p,possiblePoints)] 
        #this method for legend detection isn't working very well now.
        points=possiblePoints
        if len(points)>20:  
            commonCurvePoints.append((points,curvePointsDict[k][1]))
    ''' 
    for ccp,k in zip(commonCurvePoints,curvePointsDict.keys()):
        svgDir="testsvgs/hassan-Figure-2"
        im=imread(svgDir+"/"+os.path.split(svgDir)[-1]+"-Curve-"+str(curvePointsDict[k][1]['Curve'])+".png")
        #print ccp
        for p in ccp[0]:
            #print p 
            im[p[1]:p[1]+6,p[0]:p[0]+6]=[255,0,0] 
        show_img(im) 
    '''
    return commonCurvePoints
        
def getTrend(points):
    sp=sorted(points, key=lambda tup: tup[0])
    #print [(p[0],p[1]) for p in sp]
    increases=0
    decreases=0
    stable=0
    for i in range(len(sp)-1):
        if sp[i][1]>sp[i+1][1]:
            increases+=1
        elif sp[i][1]<sp[i+1][1]:
            decreases+=1
        else:
            stable+=1
    stable=max(0,stable-20) #correction for legend region
    for i,x in enumerate([increases,decreases,stable]):
        if x>= 0.5*(increases+decreases+stable):
            return (i,None,None)   
    else:
        total=increases+decreases+stable 
        return (round(100*(increases/total)),round(100*(decreases/total)),round(100*(stable/total)))    
  
     
def main():
    jsonLoc=sys.argv[1]
    svgLoc=sys.argv[2]

    createCurves(svgLoc)
    if not os.path.exists(svgLoc[:-4]):
        print "svg curve separation unsuccessful, exiting";
        sys.exit(1)
    svgcurves=[svgLoc[:-4]+"/"+x for x in os.listdir(svgLoc[:-4]) if 'Curve' in x and x.endswith('svg')]
    if len(svgcurves)==0:
        print "svg curve seperation unsuccessful, exiting";
        sys.exit(1)

    tree = ET.ElementTree(file=svgLoc)
    root = tree.getroot()
    W=int(float(root.get('width')))
    H=int(float(root.get('height')))

    for x in svgcurves:  createPng(x,W,H);
    pngcurvelocs=[svgLoc[:-4]+"/"+x for x in os.listdir(svgLoc[:-4]) if 'Curve' in x and x.endswith('png')]
    
    curvePointsDict={}
    absTrends=['increasing','decreasing','alternate']
    try:
        legends=json.load(open(jsonLoc))['Legends']
        for legend in legends:
            if 'Curve' in legend:
                curvePointsDict[legend['Curve']]=(getPointsSingleCurve(svgLoc,legend['Curve']),legend)
        if len(curvePointsDict.keys())==0:
            print "no legend associated with a curve"
            sys.exit(1) 
        else:
            ccpsLegends=getCommonCurvePoints(curvePointsDict)
            if len(ccpsLegends)>0:
                for curveLegend in ccpsLegends:
                    curve=curveLegend[0]
                    legend=curveLegend[1]
                    trend=getTrend(curve)
                    trendString=""
                    if trend[1] is None: 
                        trendString=' '.join(["Curve",legend['Text'],"has",absTrends[trend[0]],"trend"])
                    else:
                        trendString=' '.join(["Curve",legend['Text'],"is", str(trend[0]),"% increasing", \
                        str(trend[1]), "% decreasing", str(trend[2]),"% stable"])
                    print trendString
            else:
                print "Not sufficient common points for the curves"        
              
    except KeyError:
        print 'Legend regions not found in the JSON, exiting'
        sys.exit(1)
        
if __name__ == "__main__":
    main() 
