import os,sys
import rsvg
import cairo
import xml.etree.cElementTree as ET
from CurveSeperation import separateCurves
import json
from skimage.io import imread
from skimage.color import rgb2hsv
import numpy as np
from PIL import Image
#def associateCurve(jsonLoc,svgLoc)
from matplotlib import pyplot as plt
import pylab 
from pprint import pprint
from munkres import Munkres

INF=99999

def createCurves(svgLoc):
    separateCurves(svgLoc)

def show_img(img):
     width = img.shape[1]/75.0
     height = img.shape[0]*width/img.shape[1]
     f = plt.figure(figsize=(width, height))
     plt.imshow(img)
     pylab.show()

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


def curveScore(l,curve):
    lb=l['TextBB']
    elbl=[lb[0]-20,lb[1],lb[0],lb[3]]
    elbr=[lb[0],lb[1],lb[2]+20,lb[3]]
    cindex=int(curve[0]) 
    cdata=curve[1]
    #img=cdata[elb[1]:elb[3],elb[0]:elb[2]]
    imgl=cdata[elbl[1]:elbl[3],elbl[0]:elbl[2]]
    imgr=cdata[elbr[1]:elbr[3],elbr[0]:elbr[2]]
    
    #print cindex,l['Text']
    #show_img(imgl)
    #show_img(imgr)    
    #points from the rectangle to the left and right of the legend word that are not white or black pixels. 
    lnzps=np.where(np.logical_and(np.greater_equal(imgl[:,:,1],0.06),np.greater_equal(imgl[:,:,2],0.1))) 
    rnzps=np.where(np.logical_and(np.greater_equal(imgr[:,:,1],0.06),np.greater_equal(imgr[:,:,2],0.1)))
    
    if len(lnzps[0])==0 and len(rnzps[0])==0: #this means for this legend, we did not find a single pixel from the 
    #curve that is to the left or right of it.
        #print l['Text'],"has no points to the left or right for",cindex
        return (None,None,None)
    elif len(lnzps[0])!=0 and len(rnzps[0])==0:
        #print l['Text'],"has curve",cindex,"to the left of it, distance:",100-np.sort(lnzps[0])[-1]
        return(cindex,'l',20-np.sort(lnzps[0])[-1])
    elif len(lnzps[0])==0 and len(rnzps[0])!=0:
        #print l['Text'],"has curve",cindex,"to the right of it, distance:",np.sort(rnzps[0])[0]
        return(cindex,'r',np.sort(rnzps[0])[0])
    else: #this means, some points from this curve belongs to both left and the right of the legend. That is improbable.
        print "Something wrong, a single curve has pixels on both sides of the image "
        return (None,None)
      
def legendCurveDictionary(legends,curveLocs):
    #print curveLocs 
    curves=[(x.split("Curve-")[1].split(".png")[0],rgb2hsv(imread(x))*360) for x in curveLocs]
    lcd={}
    for i,l in enumerate(legends):
        lcd[i]=[x for x in [curveScore(l,curve) for curve in curves] if x[1] is not None]
    return lcd   

def associateCurveLegend(D,legends):
    legendIndices=D.keys()
    curveIndices=[]
    for x in D.keys():
        for y in D[x]:
            curveIndices.append(int(y[0]))
    curveIndices=list(set(curveIndices))
    print len(legendIndices),len(curveIndices)
    cDict={}
    lDict={}
    ccDict={}
    for i,x in enumerate(legendIndices):
        lDict[i]=x
    for i,x in enumerate(curveIndices):
        cDict[i]=x
        ccDict[x]=i

    #pprint(cDict)
    #pprint(lDict)
    costMatrix=[]
    for i in range(len(legendIndices)):
        legendCost=[INF]*max(len(curveIndices),len(legendIndices))  
        curveIndicesThisLegend=[ccDict[x[0]] for x in D[lDict[i]]]
        curveValuesThisLegend=[x[2] for x in D[lDict[i]]]
        for index,curveIndex in enumerate(curveIndicesThisLegend):
            legendCost[curveIndex]=curveValuesThisLegend[index]
        #print "iteration",i,"legend",lDict[i],"has curves",curveIndicesThisLegend
        costMatrix.append(legendCost)
  
    for i in range(0,len(curveIndices)-len(legendIndices)):
        costMatrix.append([INF]*max(len(curveIndices),len(legendIndices))) 
       
    #pprint(costMatrix)
    print np.array(costMatrix).shape
    m = Munkres()
    indexes = m.compute(costMatrix)
    return [(lDict[pair[0]],cDict[pair[1]]) for pair in indexes if pair[0] in lDict and pair[1] in cDict] 

def createLegendAssociatedImage(legend,curveNumber,dir):
    im=Image.open(dir+"/"+os.path.split(dir)[-1]+"-Curve-"+str(curveNumber)+".png")
    
       

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
           if len(D[l])==0:
               del D[l]
        #pprint(D)
        #for l in D.keys():      
        #    print "legend",l,legends[l]['Text'],"has curves at distances",D[l]
        clAssociation=associateCurveLegend(D,legends) 
        for pair in clAssociation:
            print legends[pair[0]]['Text'], "is associated with curve",pair[1]
            createLegendAssociatedImage(legend=legends[pair[0]],curveNumber=pair[1],dir=svgLoc[:-4]) 
    except KeyError:
        print 'Legend regions not found in the JSON, exiting'
        sys.exit(1)
      

if __name__=="__main__":
    main()
        
       
