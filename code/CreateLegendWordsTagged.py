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
    orgPngDir="./testpngs/"
    wcPngDir="./testpngs/"
     
    jsonLoc=sys.argv[1]
    js=json.load(open(jsonLoc))
 
    im=Image.open(orgPngDir+os.path.split(jsonLoc)[1][:-12]+".png")

    draw = ImageDraw.Draw(im)

    for imt in js['ImageText']:
        if imt['TextLabel']=='legend':
            draw.rectangle(imt['TextBB'],outline="blue")
    
    im.save(wcPngDir+os.path.split(jsonLoc)[1][:-5]+".png")     
     
if __name__=="__main__":
    main()
