import time
import ctypes
import os
import pdb

from lib.morai_udp_parser import udp_parser

# MORAI simulator IP
#IP = '127.0.0.1' 
#IP = '163.152.162.57'
IP = '163.152.20.61'
PORT = 7505

def main():
    SurVehicelStatus = udp_parser(IP, PORT)
    while True :
        status = SurVehicelStatus.get_data()
        print_ego_vehicle_status(status)        
        time.sleep(0.5)

def print_ego_vehicle_status(status):
    for field_name, _ in status._fields_:
        value = getattr(status, field_name)
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        elif isinstance(value, ctypes.Array):
            value = list(value)
        print(f"{field_name}: {value}")        

    print('='*50)



if __name__ == '__main__':
    main()
