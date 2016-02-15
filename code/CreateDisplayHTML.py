import os
import sys

def main():
    sS="<!DOCTYPE html>\n<html>\n<body>\n"
    svgDir=os.path.abspath(sys.argv[1][:-4])

    sS+="<h2> Original Image </h2>\n"
    sS+="<img src=\""+svgDir+".svg"+"\" border=\"2\">\n"
 
    svgFiles=[svgDir+"/"+x for x in os.listdir(svgDir) if x.endswith("svg") and 'Curve' in x]
    sS+="<h2> Extracted Curves: SVG </h2>\n"
    for x in svgFiles:
        sS+="<img src=\""+x+"\" border=\"2\">\n"
  
    pngFiles=[svgDir+"/"+x for x in os.listdir(svgDir) if x.endswith("png") and 'Curve' in x]
    sS+="<h2> Extracted Curves converted into PNG </h2>\n"
    for x in pngFiles:
        sS+="<img src=\""+x+"\" border=\"2\">\n"
    
    with open(svgDir+".html","w") as f:
        f.write(sS+"</body>\n</html>\n") 

if __name__=="__main__":
    main()    


