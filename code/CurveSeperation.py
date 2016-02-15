import xml.etree.cElementTree as ET
import sys
import os

def getColorFromStyle(styleString):
    if 'fill:none' in styleString:
        return styleString.split("stroke:")[1].split(";")[0]
    else:
        return None

def writeSingleColorSVGs(dir,cDict,svgStartString,svgEndString):
    for index,c in enumerate([x for x in cDict.keys() if x != "#000000"]):
        ps=cDict[c]
        #print len(ps)
        con=""
        for p in ps:
            con+=p
         
        fL=dir+"/"+dir.split("/")[-1]+"-Curve-"+str(index)+".svg"
        with open(fL,"w") as f:
            f.write(svgStartString+con+svgEndString)
        #print fL,"written"       
            
def main():
    svgLoc=sys.argv[1]
    tree = ET.ElementTree(file=svgLoc)
    root = tree.getroot()
    colorDict={}
    b='{http://www.w3.org/2000/svg}'
    for path in tree.iter(b+'path'):
        color=getColorFromStyle(path.get('style')) 
        if color is not None:
            if color in colorDict:
                colorDict[color].append(ET.tostring(path))
            else:   
                colorDict[color]=[ET.tostring(path)]
    
    if not os.path.exists(svgLoc[:-4]) or not os.path.isdir(svgLoc[:-4]):
        os.mkdir(svgLoc[:-4])

    svgStartString='\n'.join(open(svgLoc).read().split("\n")[:5])
    svgEndString='\n'.join(open(svgLoc).read().split("\n")[-3:])

    writeSingleColorSVGs(svgLoc[:-4],colorDict,svgStartString+"\n",svgEndString)  

if __name__=="__main__":
    main() 
