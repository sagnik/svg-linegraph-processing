time for f in ../data/wctrlcclacsjsons/*-lc-cla-cs.json; do y=`basename $f`; z="../data/svgs/"${y:0:${#y}-22}".svg"; echo $z; python CreateDisplayHTML.py $z $f; echo "--------------------------------------"; done 

