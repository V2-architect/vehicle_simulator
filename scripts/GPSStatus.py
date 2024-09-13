import time
import ctypes
import os
import pdb

from lib.morai_udp_parser import udp_parser

# MORAI simulator IP
#IP = '127.0.0.1' 
#IP = '163.152.162.57'
IP = '163.152.20.61'
PORT = 9091

def main():
    gpsStatus = udp_parser(IP, PORT)
    while True :
        status = gpsStatus.get_gps_data()
        print_status(status)        
        time.sleep(0.5)

def print_status(status):
    for k, v in status.items():
        print(f"{k}: {v}")        
 
    print('='*50)



if __name__ == '__main__':
    main()
