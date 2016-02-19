import os,sys
import rsvg
import cairo
import xml.etree.cElementTree as ET
from CurveSeperation import separateCurves

#def associateCurve(jsonLoc,svgLoc)

def createCurves(svgLoc):
    separateCurves(svgLoc)

def createPng(svgLoc,W,H):
    img = cairo.ImageSurface(cairo.FORMAT_RGB24, int(W),int(H))
    ctx = cairo.Context(img)
    handle= rsvg.Handle(None, str(open(svgLoc).read()))
    handle.render_cairo(ctx)
    img.write_to_png(svgLoc[:-4]+".png")


def main():
    jsonLoc=sys.argv[1]
    svgLoc=sys.argv[2]
    
    createCurves(svgLoc)
    if not os.path.exists(svgLoc[:-4]): 
        print "svg curve separation unsuccessful, exiting"; 
        sys.exit(1) 
    svgcurves=[svgLoc[:-4]+"/"+x for x in os.listdir(svgLoc[:-4])]
    
    tree = ET.ElementTree(file=svgLoc)
    root = tree.getroot()
    W=int(float(root.get('width')))
    H=int(float(root.get('height')))
 
    if len(svgcurves)==0: 
        print "svg curve seperation unsuccessful, exiting"; 
        sys.exit(1) 
    for x in svgcurves: 
        print x
        createPng(x,W,H)  

if __name__=="__main__":
    main()
        
       
