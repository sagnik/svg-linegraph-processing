#code to change the Coordinate system of a JSON.

#png from svg means the PNG image file was created from the SVG using InkScape,
#else it was crop from the PDF. For some JSONs in our system, (ones in the data/modjsons
# folder), the corresponding png image (in data/pngs folder) is cropped and the 
# coordinate system in the JSON and the PNG is the same. For the other JSONs, 
# the coordinate system needs to be changed. If the PNG was cropped from the PDF, only 
# translation suffices else, both translation and scaling is needed.

from __future__ import division
import os,sys
import xml.etree.cElementTree as ET
import json

def main(): 
    jsonLoc=""
    svgLoc=""
    
    jsonCordChanged=True
    pngcropped=True

    if len(sys.argv)==3:
        jsonLoc=sys.argv[1]
        svgLoc=sys.argv[2]
        jsonCordChanged=False
        pngcropped=False
 
    elif len(sys.argv)==2:
        jsonLoc=sys.argv[1]
        jsonCordChanged=False

    else:
        print sys.argv[0],"needs at least one argument"
        sys.exit(1)

    js=json.load(open(jsonLoc))
       
    if not jsonCordChanged:
        iB=js['ImageBB']
        for i,t in enumerate(js['ImageText']):
            tB=t['TextBB']
            js['ImageText'][i]['TextBB']=[tB[0]-iB[0],tB[1]-iB[1],tB[2]-iB[0],tB[3]-iB[1]]
    
    if not pngcropped:
        #For some reason, we increased the figBB and translated all paths by 5
        #while creating the SVG file. See the first apply method in 
        #https://github.com/sagnik/svgimagesfromallenaipdffigures/blob/master/src/main/scala/edu/ist/psu/sagnik/research/svgimageproducer/writers/SVGWriter.scala
        #Those translation changes need to be accounted here.
        
        tree = ET.ElementTree(file=svgLoc)
        root = tree.getroot()

        svgH=float(root.get('height'))
        svgW=float(root.get('width'))

        tX=js['ImageBB'][0]
        tY=js['ImageBB'][1]

        pngW=js['ImageBB'][2]-js['ImageBB'][0]
        pngH=js['ImageBB'][3]-js['ImageBB'][1]

        if abs((pngW/(svgW-5)) - (pngH/(svgH-5)))>0.1:
            print "ratios are wrong, exiting"
            sys.exit(1)

        tR=(svgW-5)/pngW#transform ratio                     
        
        for i,t in enumerate(js['ImageText']):
            tB=t['TextBB']
            js['ImageText'][i]['TextBB']=[x*tR+5 for x in tB] 
          
   
    json.dump(js,open(jsonLoc[:-5]+"-tr.json","wb"))    
        
if __name__=="__main__":
    main()
  
