import json
import os,sys

def main():
    trJsonLoc=sys.argv[1]
    wcpJsonLoc="../data/old-data/wcjsons/"+os.path.split(trJsonLoc)[-1][:-8]+"-mod-wcp.json"
    trwcpJsonLoc="../data/wctrjsons/"+os.path.split(trJsonLoc)[-1][:-8]+"-tr-wcp.json"

    if not os.path.exists(wcpJsonLoc):
        print "classified JSON doesn't exist, removing",trJsonLoc 
        os.remove(trJsonLoc)
        sys.exit(1)
        
    j1=json.load(open(trJsonLoc))
    j2=json.load(open(wcpJsonLoc))
     
    if len(j1['ImageText'])!=len(j2['ImageText']):
        print "lengths don't match"
    
    for i,t in enumerate(j2['ImageText']):
        j1['ImageText'][i]['TextLabel']=t['TextLabel']
        j1['ImageText'][i]['TextLabelConf']=t['TextLabelConf']
    
    json.dump(j1,open(trwcpJsonLoc,"wb")) 

if __name__=="__main__":
    main()         
