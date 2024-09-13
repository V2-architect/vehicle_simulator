import time
import ctypes
import os
import pdb

from lib.morai_udp_parser import udp_parser

# MORAI simulator IP
#IP = '127.0.0.1' 
#IP = '163.152.162.57'
IP = '163.152.20.61'
PORT = 9102

def main():
    intersectionStatus = udp_parser(IP, PORT)
    while True :
        status = intersectionStatus.get_data()
        print_status(status)        
        time.sleep(0.5)

def print_status(status):
    for field_name, _ in status._fields_:
        value = getattr(status, field_name)
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        elif isinstance(value, ctypes.Array):
            value = list(value)
        print(f"{field_name}: {value}")        

        if field_name == 'intersection_status':
            pass
            '''
            tl_type = {
                0: '3구(R--Y--G)',
                1: '3구(R--Y--Gleft)',
                2: '4구(R--Y--Gleft--G)',
                100: '(Y--Y--Y)',
            }
            print(f'traffic_light_type: {tl_type.get(value, "unknown_type")}')
            '''
 
    print('='*50)



if __name__ == '__main__':
    main()
