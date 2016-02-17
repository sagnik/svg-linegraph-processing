import os, sys
import json

def combineLegend(jsonLoc,ImageLoc):
    lWs=[x for x in open(jsonLoc)['ImageText'] if x['TextLabel']=='legend']
    while lW in lWs:
        pWs=mergeScores()  

