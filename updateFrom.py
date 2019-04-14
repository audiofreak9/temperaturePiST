#!/usr/bin/python3

import sys
import glob
import re
from io import BytesIO
import json
import pprint
import requests
import time
import subprocess
import os
import calendar
import requests

#client id and client secret
client = 'b020c04b-731c-4121-9809-5dcc4866452f'
access_token='75860893-46a9-4a73-b6dc-e2926207093c'
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')
device_file = []
for i in range(0,2): 
        print device_folder[i]
        device_file.append(device_folder[i]+'/w1_slave')

def read_temp_raw(i):
    catdata = subprocess.Popen(['cat',device_file[i]],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = catdata.communicate()
    out_decode = out.decode('utf-8')
    lines = out_decode.split('\n')
    return lines

def read_temp(i):
    lines = read_temp_raw(i)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 33.7
        return temp_f

def getDeviceId(i):
    deviceId = os.path.basename(os.path.normpath(device_folder[i]))
    return deviceId

def main():
    endpoints_url = "https://graph.api.smartthings.com/api/smartapps/endpoints/%s?access_token=%s" % (client, access_token)
    print(endpoints_url)
    r = requests.get(endpoints_url)
    if (r.status_code != 200):
       print("Error: " + r.status_code)
    else:
       theendpoints = json.loads( r.text )       
       for i in range(0,2):
         print (i)
         temp_f = read_temp(i)
         deviceId = getDeviceId(i)
         print (deviceId)
         print (temp_f)
         print("deviceId: " + str(deviceId)+ " TempF: " + str(temp_f))
         for endp in theendpoints:
            uri = endp['uri']
            temp_url = uri + ("/update/" + str(deviceId)+ "/%.2f/F" % temp_f)
            headers = { 'Authorization' : 'Bearer ' + access_token }
            r = requests.put(temp_url, headers=headers)

       quit()

main()
