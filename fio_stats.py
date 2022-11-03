#!/usr/bin/python3.6
import sys
import string
import re
import pprint
import array as arr
import pandas as pd
import csv
import matplotlib.pyplot as plt
import xlsxwriter as xc
from os import listdir
from os.path import isfile, join
import math


#pd.set_option('display.max_columns', None)


#file_name=sys.argv[1]
dir=sys.argv[1]

def bandwidth_conversion(line):
   bandwidth = (line.split(','))[1].split(' ')[1].split('=')[1]
   if 'Mi' in bandwidth:
       bandwidth = bandwidth.split('M')[0]
   elif 'Ki' in bandwidth:
       bandwidth = float(bandwidth.split('K')[0]) / 2**10
   elif 'Gi' in bandwidth:
       bandwidth = float(bandwidth.split('K')[0]) * 2**20
   elif 'Ti' in bandwidth:
       bandwidth = float(bandwidth.split('K')[0]) * 2**30
   return bandwidth

def io_conversion(line):
   io = line.split(',')[0].split('=')[1]
   if 'k' in io:
       io = int( float(io[0:-1]) * 10**3)
   elif 'm' in io:
       io = int( float(io[0:-1]) * 10**6)
   return io


def lat_conversion(line):
    lat = ((float(line.split(',')[2].split('=')[1])))
    if line[5] == 'u':
        lat = lat / 10**3
    elif line[5] == 'n':
        lat = lat / 10**6
    elif line[5] == 's':
        lat = lat * 10**3
    return lat


def read_data(dir):
	p=0
	reads=0
	rd_latency=0
	rd_bandwidth=0
	writes=0
	wrt_bandwidth=0
	wrt_latency=0
	r=0
	w=0
	parsed_line=[]
	fio_data=[]
	fio_files = [f for f in listdir(dir) if isfile(join(dir, f))]
	for file in fio_files:
		abs_path = ('%s/%s' % (dir,file))
		rdf=open(abs_path,'r')
		reads=0
		rd_bandwidth=0
		rd_latency=0
		writes=0
		wrt_bandwidth=0
		wrt_latency=0
		for line in rdf:
			line=line.strip()
			if ('IO depths' in line):
				break
			if ('iodepth=' in line):
				if (p == 0):
					tmp=line.split('iodepth=')
					p+=1
					iodepth=tmp[1]
				else:
					p=0
			if ('read: IOPS' in line):
				rd_bandwidth=bandwidth_conversion(line)
				reads=io_conversion(line)
			if (line[0:3] == 'lat' and reads != 0 and r == 0 and 'percentiles' not in line and '%' not in line):
				rd_latency=lat_conversion(line)
				r+=1
			if ('write: IOPS' in line):
				wrt_bandwidth=bandwidth_conversion(line)
				writes=int(io_conversion(line))
			if (line[0:3] == 'lat' and writes != 0 and 'percentiles' not in line and '%' not in line):
				wrt_latency=lat_conversion(line)
		r=0
		if('run' in file):
			tmp=file.split("run")
			tmp2=tmp[1].split("-")
			run_number=tmp2[1]
		total=int(reads)+int(writes)
		tmp=int(reads)/total
		read_percent=math.ceil(tmp*100)
		fio_data=[str(read_percent),str(iodepth),str(run_number),str(reads),str(rd_bandwidth),str(rd_latency),str(writes),str(wrt_bandwidth),str(wrt_latency)]
		print(fio_data)
		parsed_line.append(fio_data)
	fio_df=pd.DataFrame(parsed_line,columns=['read_percent','iodepth','run_number','reads','reads_bw_MiBs','read_lat_ms','writes','writes_bw_MiBs','write_lat_ms'])	
	#print(fio_df)				
	return fio_df					
				
			
	 
	

def create_excel_spreadsheet():
	cell_loc=['A','M']
	iodepth=arr.array('L',[1,16,32,48,64,80,96,112,128,256,512])
	icount=len(iodepth)
	i=0
	a=2
	r=0
	z=0
	c=0
	workbook=xc.Workbook('baseline__no_nconnect.xlsx')
	worksheet=workbook.add_worksheet()
	#u=int(icount/2)
	#while (z <= 11):
	while(r < 125):
		while (i < icount):
			cell_location=str(cell_loc[c]) + str(a)
			#print("Cell" + str(cell_location) + "Read%" + str(r) + "Iodepth" + str(iodepth[i]) + "\n")
			worksheet.insert_image(cell_location,'read_percent_{}_iodepth_{}.csv.png'.format(r,iodepth[i]),{'x_scale': 0.5, 'y_scale': 0.5})
			c=c+1
			i=i+1
			if(i !=11):
				cell_location=str(cell_loc[c]) + str(a)
				#print("Cell" + str(cell_location) + "Read%" + str(r) + "Iodepth" + str(iodepth[i]) + "\n")
				worksheet.insert_image(cell_location,'read_percent_{}_iodepth_{}.csv.png'.format(r,iodepth[i]),{'x_scale': 0.5, 'y_scale': 0.5})
			c=0
			a=a+20
			i=i+1
		i=0
		r=r+25
	workbook.close()



def graph_data(file,r,j):
	
	i=j
	print(file,r,j)	
	fio_t=pd.read_csv(file)
	fig,ax = plt.subplots(figsize=(15,6),dpi=80)
	plt.title("Throughput and Latency\n Reads={}% Iodpeth={}".format(r,i))
	ax2=ax.twinx()
	if r == 0:
		l1=ax.plot(fio_t.run_number,fio_t.writes_bw_MiBs, label='Write Throughput',color='blue')
		l2=ax2.plot(fio_t.run_number,fio_t.write_lat_ms,label='write_latency',color='red')
		lgs=l1 + l2
	elif r == 100:
		l1=ax.plot(fio_t.run_number,fio_t.reads_bw_MiBs, label='Read Throughput',color='green')
		l2=ax2.plot(fio_t.run_number,fio_t.read_lat_ms,label='read_latency',color='orange')
		lgs=l1 + l2
	else:
		l1=ax.plot(fio_t.run_number,fio_t.reads_bw_MiBs, label='Read Throughput',color='green')
		l2=ax2.plot(fio_t.run_number,fio_t.read_lat_ms,label='read_latency',color='orange')
		l3=ax.plot(fio_t.run_number,fio_t.writes_bw_MiBs, label='Write Throughput',color='blue')
		l4=ax2.plot(fio_t.run_number,fio_t.write_lat_ms,label='write_latency',color='red')
		lgs=l1 + l2 + l3 + l4
	lns=[l.get_label() for l in lgs]
	ax.legend(lgs,lns,loc=0)
	ax.set_xlabel('runs')
	ax.set_ylabel('Throughput MB/s',color='blue')
	ax2.set_ylabel('Latency ms',color='red')
	ax2.set_ylim(0,30)
	plt.xticks(fio_t.run_number)
	ax.grid()
	fig.savefig('{}.png'.format(file))
	plt.close()
	#plt.show()




def parse_data(fio_df):
	x=0
	r=0
	iodepth=arr.array('L',[1,16,32,48,64,80,96,112,128,256,512])
	icount=len(iodepth)
	i=0
	run=1
	y=60
	z=0
	row=""
	data=[]
	fio_df.to_csv("fio_converted_data.csv", encoding="utf-8",index=False)
	fioData=pd.read_csv("fio_converted_data.csv")
	d=fioData.sort_values(by=['read_percent','iodepth','run_number'])
	d.to_csv("fio_data_sorted.csv",encoding='utf-8',index=False)
	count=len(d.index)
	
	while (r < 125):
		while ( i < icount):
			g=d.iloc[z:y,0:9]
			file="read_percent_{}_iodepth_{}.csv".format(r,iodepth[i])
			g.to_csv(file,encoding='utf-8',index=False)
			j=iodepth[i]
			graph_data(file,r,j)
			z=y
			y=y+60
			i=i+1
		i=0
		r=r+25
		
		
def convert_csv(file_name):
	fd=open(file_name,"r")	
	fdr=fd.readlines()
	x=1
	y=0
	fio_data=[]
	fd=[]
	count=len(fdr)
	while (x < count):
		replace_dashes=fdr[x].replace("-",',')
		fill_empty_fields=replace_dashes.replace(',,',',0,')
		temp1=fill_empty_fields.replace(',,',',0,')
		temp2=temp1.split("\n")
		missing=temp2[0].count(',')
		if (missing == 12):
			temp4=str(temp2[0]) + "," + "," + ","
			#temp5=temp4.replace(',,',',0,')
			temp3=temp4.split(",")
		else:
			temp3=temp2[0].split(",")
		fio_data.append(temp3)
		x=x+1
	fio_df=pd.DataFrame(fio_data,columns=['fio1','fio2','fio3','fio4','fio5','read_percent','iodepth','iodepth_number','run','run_number','reads','reads_bw_MiBs','read_lat_ms','writes','writes_bw_MiBs','write_lat_ms'])
	fio_df['total throughput MiBs']=fio_df['reads_bw_MiBs'] + fio_df['writes_bw_MiBs']
	d=fio_df.to_csv("fio_converted_data.csv", encoding='utf-8',index=False)	
	return 


def main():
	fio_df=read_data(dir)
	#convert_csv(file_name)
	parse_data(fio_df)
	create_excel_spreadsheet()

main()


