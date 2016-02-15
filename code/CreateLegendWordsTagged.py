from PIL import Image,ImageDraw
import json
import os,sys

def main():
    dataDir="../data/"
    orgPngDir=dataDir+"pngs/"
    wcPngDir=dataDir+"wcpngs/"
    
    jsonLoc=sys.argv[1]
    
    im=Image.open(orgPngDir+os.path.split(jsonLoc)[1][:-9]+".png") 
    draw = ImageDraw.Draw(im)

    js=json.load(open(jsonLoc))
    for imt in js['ImageText']:
        if imt['TextLabel']=='legend':
            #print imt['Text'],imt['TextBB']
            draw.rectangle(imt['TextBB'],outline="blue")
    
    im.save(wcPngDir+os.path.split(jsonLoc)[1][:-5]+".png")    
     
if __name__=="__main__":
    main()
