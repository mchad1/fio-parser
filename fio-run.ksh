#!/usr/bin/ksh

if [[ -z $1 ]]; then
    echo "Please enter a base directory for output and config files"
    exit
else
    base_dir=$1
fi

workingset=1TBWorkingset
size=crap
iodepth=crap
bs=crap
rw=crap
rwmixread=crap
max=crap
job=crap
#./ip-collect $1
#for count in 32 16 8 4 2 1; do 
#for count in 32 1 ; do 
#for count in 5 1 ; do 
for count in 32 ; do 
    #Create Directories, exit on error"
    dir=${base_dir}/${count}vms/$workingset
    config_dir=${dir}/config
    output_dir=${dir}/output
    mkdir -p $config_dir >/dev/null 2>&1
    mkdir -p $output_dir >/dev/null 2>&1
    if [[ -z `ls $dir` ]]; then
        echo "The specified directory either does not exist or could not be accessed/created: $base_dir"
	echo "exiting"
	exit
    fi

    if [[ $count == 64 ]]; then
        #max=15
	size=1G
    elif [[ $count == 32 ]]; then
	#size=8G
	size=10M
    elif [[ $count == 16 ]]; then
	#size=10M
        size=16G
    elif [[ $count == 8 ]]; then
	#size=10M
	size=32G
    elif [[ $count == 5 ]]; then
	#size=10M
	size=52G
    elif [[ $count == 4 ]]; then
	#size=10M
	size=64G
    elif [[ $count == 2 ]]; then
	#size=10M
	size=128G
    elif [[ $count == 1 ]]; then
	size=10M
	#size=256G
    fi
    #for iosize in 64 32 16 8 4; do
    for iosize in 64 4; do
        if [[ $iosize -le 16 ]]; then
            rw=randrw
        else
            rw=rw
        fi
        #for mix in 100 50 0; do
        for mix in 100 90 80 70 60 50 40 30 20 10 0; do
        #for mix in 50; do
           if [[ $mix == 0 ]]; then
	       #max= 15
	       max=64
           elif [[ $mix = 100 ]]; then
	       if [[ $rw == "randrw" ]]; then
	           #max=40
	           max=64
	       else
		   #max=15 
		   max=64 
	       fi
	   else
	       #max=15 
	       #max=10
	       max=64
           fi
	   i=$max
	   min=0
	   (( min = max - 1 ))
	   while [[ $i -gt $min ]]; do
               echo "[global]" > config-$count
               echo "name=fio-test" >> config-$count
               echo "directory=/mnt/elastic" >> config-$count
               echo "ioengine=libaio" >> config-$count
               echo "direct=1" >> config-$count
               echo "numjobs=4" >> config-$count
               echo "nrfiles=4" >> config-$count
               #echo "runtime=600" >> config-$count
               echo "runtime=180" >> config-$count
               echo "group_reporting" >> config-$count
               echo "time_based" >> config-$count
               echo "stonewall" >> config-$count
               echo "bs=${iosize}K" >> config-$count
               echo "rw=${rw}" >> config-$count
               echo "rwmixread=${mix}" >> config-$count
               echo "iodepth=${i}" >> config-$count
               echo "size=${size}" >> config-$count
	       echo "ramp_time=20" >> config-$count
	       echo "[rw]" >> config-$count
	       echo "[randrw]" >> config-$count
	       file="vm$count-iodepth$i-filesize$size-bs$iosize-rwmix$mix"

	       #Run Stuff Here
               echo fio --client=/mnt/elastic/fio-hosts-$count --output-format=normal --output=../output/output-${file} --group_reporting --section=$rw config-${file} > ${config_dir}/command-${file}
	       cat config-$count > ${config_dir}/config-${file}
               fio --client=/mnt/elastic/fio-hosts-$count --output-format=normal --output=${output_dir}/output-$file  --group_reporting --section=$rw config-$count
	       (( i = i - 1 ))
           done 
        done
    done
    echo /mnt/elastic/fio-shutdown-post-$count
    #/mnt/elastic/fio-shutdown-post-$count
    #/mnt/elastic/fio-stop
 done
