#!/usr/bin/python
from os import listdir
from os.path import isfile, join
import argparse
import json
import os
import sys

def command_line():
    parser = argparse.ArgumentParser(prog='fio-parser.py',description='%(prog)s is used to parse fio output files')
    parser.add_argument('--directory','-d',type=str,help='Specify the directory with fio output files to parse.  If none if provided, ./ is used')
    arg = vars(parser.parse_args())

    if not arg['directory']:
        directory=os.getcwd()
    else:
        directory=arg['directory']
    file_list = get_file_list(directory)
    return file_list

def get_file_list(directory):
    '''
    extract the contents of the current file if present to only overwrite the section in play
    '''
    if os.path.exists(directory):
        file_list=[]
        onlyfiles = [ files for files in listdir(directory) if isfile(join(directory,files))]
        #Check for non binary files and make a list of them
        for files in onlyfiles:
            abs_path = ('%s/%s' % (directory,files))
            with open( abs_path,'rb') as fh:
                if b'\x00' not in fh.read():
                    file_list.append('%s/%s' % (directory,files))
        if (len(file_list)) > 0:
            return file_list
        else:
            print('No text files found')
            exit()
    else:
        print('Directory %s invalid' % (directory))
        exit()

def parse_files(file_list):
    for working_file in file_list:
        with open( working_file,'r') as fh:
            file_content = fh.readlines()
        extract_content(file_content, working_file)

def bandwidth_conversion(line):
   bandwidth = (line.split(','))[1].split(' ')[1].split('=')[1]
   if 'Mi' in bandwidth:
       bandwidth = bandwidth.split('M')[0]
   elif 'Ki' in bandwidth:
       bandwidth = int(bandwidth.split('K')[0]) / 2**10 
   elif 'Gi' in bandwidth:
       bandwidth = int(bandwidth.split('K')[0]) * 2**20 
   elif 'Ti' in bandwidth:
       bandwidth = int(bandwidth.split('K')[0]) * 2**30 
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
        
  

def extract_content(content, working_file):
    output=(working_file.split('/')[-1])
    parsed_content={}
    for line in content:
       line=line.strip()
       if 'read: IOP' in  line:
           parsed_content['read_iop']= io_conversion(line)
           parsed_content['read_bw'] = bandwidth_conversion(line)
       if 'read_iop' in parsed_content.keys():
           if line[0:3] == 'lat' and 'read_lat' not in parsed_content.keys():
               parsed_content['read_lat'] = lat_conversion(line)

       if 'write: IOP' in  line:
           parsed_content['write_iop']= io_conversion(line)
           parsed_content['write_bw'] = bandwidth_conversion(line)
       if 'write_iop' in parsed_content.keys():
           if line[0:3] == 'lat' and 'write_lat' not in parsed_content.keys():
               parsed_content['write_lat'] = lat_conversion(line)

    if 'read_iop' in parsed_content.keys():
        output += ((',%s,%s') % (parsed_content['read_iop'],parsed_content['read_bw']))
    if 'read_lat' in parsed_content.keys():
        output += ((',%s') % (parsed_content['read_lat']))
    if 'write_iop' in parsed_content.keys() and 'read_iop' not in parsed_content.keys():
        output += ((',,,,%s,%s') % (parsed_content['write_iop'],parsed_content['write_bw']))
    elif 'write_iop' in parsed_content.keys():
        output += ((',%s,%s') % (parsed_content['write_iop'],parsed_content['write_bw']))
    if 'write_lat' in parsed_content.keys():
        output += ((',%s') % (parsed_content['write_lat']))
    print(output)


file_list = command_line()
parse_files(file_list)

