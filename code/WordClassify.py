import sys,os
from FeatureExtractionOneFileWC import FeatureExtractOneFile as feWC
import pickle
import json
from pprint import pprint
import numpy as np

classDict={
   1:'xaxislabel',
   2:'xaxisvalue',
   3:'yaxislabel',
   4:'yaxisvalue',
   5:'legend',
   6:'figurelabel',
   7:'unknown',
}
def main():
    dataDir="../data/"
    wcJsonDir=dataDir+"wcjsons/"
    wcPngDir=dataDir+"wcpngs/"
    modelLoc=dataDir+"wordclassifymodel-rf.pickle"

    jsonLoc=sys.argv[1]
    ft=feWC(jsonLoc)
    clf=pickle.load(open(modelLoc))
    labels=[classDict[int(x)] for x in clf.predict(ft)]
    prob_matrix=clf.predict_proba(ft)
    labels_prob=[np.max(prob_matrix[x,:]) for x in range(prob_matrix.shape[0])]
    #print labels,labels_prob
    js=json.load(open(jsonLoc))
    if len(js['ImageText']) != len(labels):
        print "no. of words in JSON != no. of classified labels, exiting"
        sys.exit(1)
    else:
        for i in range(len(js['ImageText'])):
            js['ImageText'][i]['TextLabel']=labels[i]
            js['ImageText'][i]['TextLabelConf']=labels_prob[i]
    
        #pprint(js)
        wcJsonLoc=wcJsonDir+os.path.split(jsonLoc)[1][:-5]+"-wcp.json"
        json.dump(js,open(wcJsonLoc,"wb")) 
        print "written",wcJsonLoc

if __name__=="__main__":
    main()

      
