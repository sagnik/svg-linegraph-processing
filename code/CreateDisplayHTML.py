import os
import sys
import json

def main():
    sS="<!DOCTYPE html>\n<html>\n<body>\n"
    svgDir=os.path.abspath(sys.argv[1][:-4])
    wcpngLoc=os.path.abspath("../data/old-data/wcpngs/"+os.path.split(sys.argv[1])[-1][:-4]+"-mod-wcp.png")
    wcpnglcLoc=os.path.abspath("../data/wctrlcpngs/"+os.path.split(sys.argv[1])[-1][:-4]+"-tr-wcp-lc.png")
    jsonLoc=sys.argv[2]
    js=json.load(open(jsonLoc))

    sS+="\n<h2> Original Image </h2>\n"
    sS+="<img src=\""+svgDir+".svg"+"\" border=\"2\">\n"
    
    sS+="\n<h2> Summary </h2>\n" 
    sS+="<p> This plot shows "
    sS+="<b>"
    sS+=' '.join([x['Text'] for x in js['ImageText'] if x['TextLabel']=='yaxislabel'])
    sS+="</b>"
    sS+=" v/s "
    sS+="<b>"
    sS+=' '.join([x['Text'] for x in js['ImageText'] if x['TextLabel']=='xaxislabel'])
    sS+="</b>"
    sS+=" curves for following methods:"
    for i,cl in enumerate(js['CurveLegend']):
        sS+=" "+str(i+1)+". "+cl['Text']+", "
    sS+=".\n"
    sS+="<p><b>The curve trends are:</b></p>\n" 
    for cl in js['CurveLegend']:
        sS+="<p> "+cl['Trend']+" </p>\n"
    sS+="<p><b>The X axis values are: </b>" 
    sS+=','.join([x['Text'] for x in js['ImageText'] if x['TextLabel']=='xaxisvalue']) 
    sS+="</p>\n" 
    sS+="<p><b> The Y axis values are: </b>" 
    sS+=','.join([x['Text'] for x in js['ImageText'] if x['TextLabel']=='yaxisvalue']) 
    sS+="</p>\n" 
    sS+='<p> The Caption for the figure is:</p>'
    sS+=js['Caption']
    sS+="</p>"

    sS+="\n<h2> Steps </h2>\n"
     
    svgFiles=[svgDir+"/"+x for x in os.listdir(svgDir) if x.endswith("svg") and 'Curve' in x]
    sS+="\n<h3> Curve Separation </h3>\n"
    for x in svgFiles:
        sS+="<img src=\""+x+"\" border=\"2\">\n"
  
    sS+="\n<h3> Word Classification (Only Legend Words are Shown) </h3>\n"
    sS+="<img src=\""+wcpngLoc+"\" border=\"2\">\n"

    sS+="\n<h3> Combining Legend Words into Strings </h3>\n"
    sS+="<img src=\""+wcpnglcLoc+"\" border=\"2\">\n"


    pngFiles=[svgDir+"/"+x for x in os.listdir(svgDir) if x.endswith("png") and 'curve' in x]
    sS+="\n<h3> Curve Legend Association </h3>\n"
    for x in pngFiles:
        sS+="<img src=\""+x+"\" border=\"2\">\n"
    
    with open(svgDir+".html","w") as f:
        f.write(sS.encode('utf8')+"</body>\n</html>\n") 

if __name__=="__main__":
    main()    


