import time
import ctypes
import os
import pdb

from lib.morai_udp_parser import udp_parser
from lib import network_setting

def main():
    simul = Simulator()
    simul.create_instances()
    simul.start()
    while True:
        simul.status()
        simul.write_data()






    instances = simul.get_instances()
    
    for instance in instances:
        instance.run()

    while True:
        for instance in instances:
            instance.status()
            instance.write_data()

    EgoVehicleStatus = udp_parser(IP, network_setting.PORT_info['EgoVehicleStatus'])
    CollisionInfo    = udp_parser(IP, network_setting.PORT_info['CollisionInfo'])
    IntersectionInfo = udp_parser(IP, network_setting.PORT_info['IntersectionInfo'])
    SurVehicleStatus = udp_parser(IP, network_setting.PORT_info['SurVehicleStatus'])
    TrafficLightInfo = udp_parser(IP, network_setting.PORT_info['TrafficLightInfo'])
    GPSStatus        = udp_parser(IP, network_setting.PORT_info['GPSStatus'])

    VehicleDatas = [
        EgoVehicleStatus,
        CollisionInfo,
        IntersectionInfo,
        SurVehicleStatus,
        TrafficLightInfo,
        GPSStatus
    ]

    while True :
        for v_data in VehicleDatas:
            status = v_data.get_data()
            print_status(status)        
        time.sleep(1)

def print_status(status):
    for field_name, _ in status._fields_:
        value = getattr(status, field_name)
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        elif isinstance(value, ctypes.Array):
            value = list(value)
        print(f"{field_name}: {value}")        

        #if field_name == 'signed_vel':
        #    os.system(f"echo {value} > /home/jhshin/work/someip_app/services/VehicleSpeed/vehicle_speed.txt")
    print('='*50 + '\n')



if __name__ == '__main__':
    main()
