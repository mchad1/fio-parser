for bs in 64 4; do
 for mix in 100 0; do
 for run in 1 2 3; 
    do  ./fio-parser.py -d $1/run${run}/$2vms/1TBWorkingset/output/ | grep bs${bs}-rwmix${mix} | while read line; do
      depth=`echo $line | sed "s/-iodepth/ /g" | sed "s/-filesize/ filesize/g" | awk '{print $2}'`
      echo `hostname`,$run,$depth,$line
    done
  done
 done
done
