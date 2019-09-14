for run in 1; do 
    for i in 200 100 80 60 48 44 40 36 32 28 24 20 16 12 8 4 1; do
        /opt/fio-parser/fio-run.ksh /mnt/fio/output/$1/run${run}/ $i
    done
done
