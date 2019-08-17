#Note: Only tested with fio version 3.x

# fio-parser.py
This repository contains code used to parse fio normal output (as in non json)
As well as instructions for installing and running fio in both single and multi instance mode

usage: fio-parser.py [-h] [--directory DIRECTORY]

optional arguments:
  -h, --help            show this help message and exit
  --directory DIRECTORY, -d DIRECTORY
                        Specify the directory with fio output files to parse.
                        If none if provided, ./ is used

Output looks something like this

fio_file,reads,read_bw(MiB/s),read_lat(ms),writes,write_bw(MIB/s),write_lat(ms)
output-vm32-iodepth200-filesize8G-bs64-rwmix100,69900,4372,352.57964
output-vm32-iodepth200-filesize8G-bs64-rwmix75,38600,2416,478.70303,12900,809,494.06208
output-vm32-iodepth200-filesize8G-bs64-rwmix50,21000,1316,604.07159,21000,1316,610.97722
output-vm32-iodepth200-filesize8G-bs64-rwmix25,8636,540,695.76001,25800,1617,738.59605
output-vm32-iodepth200-filesize8G-bs64-rwmix0,,,,28300,1770,881.72075
output-vm32-iodepth100-filesize8G-bs64-rwmix100,65400,4089,191.61536
output-vm32-iodepth100-filesize8G-bs64-rwmix75,36100,2256,256.18691,12100,755,276.21681
output-vm32-iodepth100-filesize8G-bs64-rwmix50,22100,1380,284.67851,22100,1381,294.03005
output-vm32-iodepth100-filesize8G-bs64-rwmix0,,,,27300,1708,462.75325
output-vm32-iodepth100-filesize8G-bs64-rwmix25,8201,513,352.77054,24500,1534,403.34769

