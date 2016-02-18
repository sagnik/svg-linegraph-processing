from __future__ import division
from PIL import Image,ImageDraw
import json
import os,sys
import xml.etree.cElementTree as ET

def main():
    ''' 
    dataDir="../data/"
    orgPngDir=dataDir+"pngs/"
    wcPngDir=dataDir+"wcpngs/"
    '''
    subtractImageBB=False
    #for a single file in the "code" directory, just for testing.
    orgPngDir="./"
    wcPngDir="./"
    subtractImageBB=True 

    jsonLoc=sys.argv[1]
    js=json.load(open(jsonLoc))
 
    svgLoc=orgPngDir+os.path.split(jsonLoc)[1][:-9]+".svg"
    tree = ET.ElementTree(file=svgLoc)
    root = tree.getroot()
    svgH=float(root.get('height'))
    svgW=float(root.get('width'))

    translateString=root.findall("{http://www.w3.org/2000/svg}g")[0].get('transform') #there's going to be exactly one child
    tXSVG=abs(round(float(translateString.split("(")[1].split(",")[0])))
    tYSVG=abs(round(float(translateString.split("(")[1].split(",")[1].split(")")[0])))
    #print tX,tY,translateString
    
            
    im=Image.open(orgPngDir+os.path.split(jsonLoc)[1][:-9]+".png")

    tX=js['ImageBB'][0]
    tY=js['ImageBB'][1]
    
    pngW=js['ImageBB'][2]-js['ImageBB'][0]
    pngH=js['ImageBB'][3]-js['ImageBB'][1]

    if abs(pngW/svgW - pngH/svgH)>0.1:  
        print "ratios are wrong, exiting"
        sys.exit(1)

    tR=svgW/pngW#transform ratio 

    draw = ImageDraw.Draw(im)

    for imt in js['ImageText']:
        if imt['TextLabel']=='legend':
           if subtractImageBB:
                a=imt['TextBB']
                b=[(a[0]-tX)*tR,(a[1]-tY)*tR,(a[2]-tX)*tR,(a[3]-tY)*tR]
                #print imt['Text'],imt['TextBB'],b
                draw.rectangle(b,outline="blue")
           else:
                draw.rectangle(imt['TextBB'],outline="blue")
    
    im.save(wcPngDir+os.path.split(jsonLoc)[1][:-5]+".png")     
     
if __name__=="__main__":
    main()
