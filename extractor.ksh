for bs in 64 4; do
 for mix in 100 0; do
 for run in 1 2 3; 
    do  ./fio-parser.py -d $1/run${run}/$2vms/1TBWorkingset/output/ | grep bs${bs}-rwmix${mix} | while read line; do
      depth=`echo $line | sed "s/-iodepth/ /g" | sed "s/-filesize/ filesize/g" | awk '{print $2}'`
      shortline=`echo $line | cut -d, -f2,3,4,5,6,7,8`
      dir=`echo $1 | sed "s#/# #g" | wc -w`
      (( dir = dir + 1 ))
      dir=`echo $1 | cut -d/ -f$dir`
      echo $dir,$run,$depth,$shortline
    done
  done
 done
done
