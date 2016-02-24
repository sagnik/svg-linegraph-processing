time for f in ../data/wctrlcclajsons/*-lc-cla.json; do y=`basename $f`; z="../data/svgs/"${y:0:${#y}-19}".svg"; echo $z; python CurveSummarization.py $f $z; echo "--------------------------------------"; done >> logs/curveSummarization.log

