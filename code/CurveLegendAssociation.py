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
    elbl=[lb[0]-200,lb[1],lb[0]-5,lb[3]]
    elbr=[lb[0]+5,lb[1],lb[2]+200,lb[3]]
    cindex=curve[0] 
    cdata=curve[1]
    #img=cdata[elb[1]:elb[3],elb[0]:elb[2]]
    imgl=cdata[elbl[1]:elbl[3],elbl[0]:elbl[2]]
    imgr=cdata[elbr[1]:elbr[3],elbr[0]:elbr[2]]
    
    #points from the rectangle to the left and right of the legend word that are not white or black pixels. 
    lnzps=np.where(np.logical_and(np.greater_equal(imgl[:,:,1],0.06),np.greater_equal(imgl[:,:,2],0.1))) 
    rnzps=np.where(np.logical_and(np.greater_equal(imgr[:,:,1],0.06),np.greater_equal(imgr[:,:,2],0.1)))
    
    if len(lnzps[0])==0 and len(rnzps[0])==0: #this means for this legend, we did not find a single pixel from the 
    #curve that is to the left or right of it.
        return (None,None)
    elif len(lnzps[0])!=0 and len(rnzps[0])==0:
        return(cindex,100-np.sort(lnzps[0])[-1])
    elif len(lnzps[0])==0 and len(rnzps[0])!=0:
        return(cindex,np.sort(rnzps[0])[0])
    else: #this means, some points from this curve belongs to both left and the right of the legend. That is improbable.
        print "Something wrong"
        return (None,None)
      
def legendCurveDictionary(legends,curveLocs):
    #print curveLocs 
    curves=[(x.split("Curve-")[1].split(".png")[0],rgb2hsv(imread(x))*360) for x in curveLocs]
    lcd={}
    for i,l in enumerate(legends):
        lcd[i]=[x for x in [curveScore(l,curve) for curve in curves] if x[1] is not None]
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
    
    try:
        legends=json.load(open(jsonLoc))['Legends']
        #print len(legends),len(pngcurvelocs)
        D=legendCurveDictionary(legends,pngcurvelocs) 
        for l in D.keys():
            #print D[l]
            print "legend",legends[l]['Text'],"has curves at distances",D[l] 
    except KeyError:
        print 'Legend regions not found in the JSON, exiting'
        sys.exit(1)
      

if __name__=="__main__":
    main()
        
       
