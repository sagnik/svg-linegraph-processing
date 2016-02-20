import os,sys
import rsvg
import cairo
import xml.etree.cElementTree as ET
from CurveSeperation import separateCurves
import json
from skimage.io import imread
from skimage.color import rgb2hsv
import numpy as np

#def associateCurve(jsonLoc,svgLoc)

def createCurves(svgLoc):
    separateCurves(svgLoc)

def createPng(svgLoc,W,H):
    img = cairo.ImageSurface(cairo.FORMAT_RGB24, int(W),int(H))
    ctx = cairo.Context(img)
    handle= rsvg.Handle(None, str(open(svgLoc).read()))
    handle.render_cairo(ctx)
    img.write_to_png(svgLoc[:-4]+".png")

def curveScore(l,curve):
    lb=l['TextBB']
    elbl=[lb[0]-100,lb[1],lb[0]-5,lb[3]]
    elbr=[lb[0]+5,lb[1],lb[2]+100,lb[3]]
    cindex=curve[0] 
    cdata=curve[1]
    #img=cdata[elb[1]:elb[3],elb[0]:elb[2]]
    img[np.where(img[:,:,2]<0.11)]=0
    img[np.where(img[:,:,1]<0.06)]=0
    #now the non zero pixels are only from the curve.     
       
def legendCurveDictionary(legends,curveLocs):
    print curveLocs 
    curves=[(x.split("Curve-")[1].split(".png")[0],rgb2hsv(imread(x))*360) for x in curveLocs]
    lcd={}
    for i,l in enumerate(legends):
        lcd[i]=[x[0] for x in [curveScore(l,curve) for curve in curves] if x[1]>0]
    return lcd   

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
    
    legends=[]
    try:
        legends=json.load(open(jsonLoc))['Legends']
        #print len(legends),len(pngcurvelocs)
        D=legendCurveDictionary(legends,pngcurvelocs) 
    except KeyError:
        print 'Legend regions not found in the JSON, exiting'
        sys.exit(1)
      

if __name__=="__main__":
    main()
        
       
