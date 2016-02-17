from PIL import Image,ImageDraw
import json
import os,sys

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
    
    im=Image.open(orgPngDir+os.path.split(jsonLoc)[1][:-9]+".png") 
    draw = ImageDraw.Draw(im)

    js=json.load(open(jsonLoc))
    for imt in js['ImageText']:
        if imt['TextLabel']=='legend':
            #print imt['Text'],imt['TextBB']
            if subtractImageBB:
                a=imt['TextBB']
                b=[a[0]-js['ImageBB'][0],a[1]-js['ImageBB'][1],a[2]-js['ImageBB'][0],a[3]-js['ImageBB'][1]]
                draw.rectangle(b,outline="blue")
            else:
                draw.rectangle(imt['TextBB'],outline="blue")
    
    im.save(wcPngDir+os.path.split(jsonLoc)[1][:-5]+".png")     
     
if __name__=="__main__":
    main()
