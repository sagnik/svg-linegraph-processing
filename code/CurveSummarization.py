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

def getSampleXIndices(curvePointsDict):
    curvexs=[np.unique(curvePointsDict[k][0][1]) for k in curvePointsDict]
    '''
    this is to show where the x and y points are  

    for k in curvePointsDict.keys():
        print "curve",curvePointsDict[k][1]['Curve'],"points",[(x,y) for x,y in zip(curvePointsDict[k][0][1],curvePointsDict[k][0][0])]
        svgDir="testsvgs/hassan-Figure-2"
        show_img(imread(svgDir+"/"+os.path.split(svgDir)[-1]+"-Curve-"+str(curvePointsDict[k][1]['Curve'])+".png"))
    '''
    commonCurvexs=[]
    if len(curvexs)==1:
        commonCurvexs=curvexs[0] 
    commonCurvexs=reduce(np.intersect1d,(x for x in curvexs))
    #print commonCurvexs,type(commonCurvexs)  
    commonCuvrexIndices=[]  
    for curvex in curvexs:
        #print curvex,type(curvex)
        c=[np.where((curvex==x))[0][0] for x in commonCurvexs]
        points=[(curvePointsDict[k][0][1][i],curvePointsDict[k][0][0][i]) for i in c] 
    
    for curvex,k in zip(curvexs,curvePointsDict.keys()):
        #print curvex,type(curvex)
        c=[np.where((curvex==x))[0][0] for x in commonCurvexs]
        
        points=[(curvePointsDict[k][0][1][i],curvePointsDict[k][0][0][i]) for i in c] 
        svgDir="testsvgs/hassan-Figure-2"
        im=imread(svgDir+"/"+os.path.split(svgDir)[-1]+"-Curve-"+str(curvePointsDict[k][1]['Curve'])+".png")
        random.shuffle(points)
        for p in points[0:100]:
            im[p[1]:p[1]+6,p[0]:p[0]+6]=[255,0,0] 
        show_img(im) 
        
 
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

    try:
        legends=json.load(open(jsonLoc))['Legends']
        for legend in legends:
            if 'Curve' in legend:
                curvePointsDict[legend['Curve']]=(getPointsSingleCurve(svgLoc,legend['Curve']),legend)
        if len(curvePointsDict.keys())==0:
            print "no legend associated with a curve"
            sys.exit(1) 
        else:
            samplePointXindices=getSampleXIndices(curvePointsDict)           
    except KeyError:
        print 'Legend regions not found in the JSON, exiting'
        sys.exit(1)
        
if __name__ == "__main__":
    main() 
