#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading
import ctypes
import pynmea2
import pdb

class SimulData:
    def __init__(self):
        # EgoVehicle ==========================
        #  VehicleSpeed
        self.vehicle_speed_x: float = 0
        self.vehicle_speed_y: float = 0
        self.vehicle_speed_z: float = 0
        #  VehiclePose
        self.vehicle_roll: float = 0
        self.vehicle_pitch: float = 0
        self.vehicle_yaw: float = 0
        self.angular_velocity_x: float = 0
        self.angular_velocity_y: float = 0
        self.angular_velocity_z: float = 0
        #  VehicleAccel
        self.accel_x: float = 0
        self.accel_y: float = 0
        self.accel_z: float = 0
        #  Transmission
        self.gear: int = 0
        #  Driving
        self.accel_pressure: float = 0
        self.brake_pressure: float = 0
        #  SteeringWheel
        self.steerwheel_deg: float = 0

        # SurVehicle ==========================
        #  ObjectDetection
        self.object_type: int = 0
        self.object_velocity_x: float = 0
        self.object_velocity_y: float = 0
        self.object_velocity_z: float = 0
        self.object_accel_x: float = 0
        self.object_accel_y: float = 0
        self.object_accel_z: float = 0

        # Collision ===========================
        #  Collision
        self.collision_object_type: int = 0

        # TrafficLight ========================
        #  TrafficLight
        self.traffic_light_type: int = 0
        self.traffic_light_status: int = 0

        # Intersection ========================
        #  Intersection
        self.intersection_index: int = 0
        self.intersection_status: int = 0
        self.intersection_time: float = 0

        # GPS =================================
        #  Location
        self.latitude: float = 0
        self.longitude: float = 0
        self.altitude: float = 0


class SimulDataHandler:
    # simul_data: common instance among many threads
    def __init__(self, ip, port, simul_parsed_data):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((ip,port))
        self.data_size = 65535
        self.simul_parsed_data = simul_parsed_data


        # start thread
        if port == 9091:
            threading.Thread(target=self.recv_gps_data, daemon=True).start()
        elif port in [909, 7502, 7505, 9092, 9102, 9091]:
            threading.Thread(target=self.recv_udp_data, daemon=True).start()

    def recv_udp_data(self):
        while True :
            raw_data, _ = self.socket.recvfrom(self.data_size)

            # raw data -> self.simul_parsed_data(structured data)
            ctypes.memmove(ctypes.addressof(self.simul_parsed_data), raw_data, ctypes.sizeof(self.simul_parsed_data))

    def recv_gps_data(self):
        while True :
            raw_data, _ = self.socket.recvfrom(self.data_size)
            asciiDatas = raw_data.decode('ascii')
            gpsdatas = asciiDatas.split('\r\n')[0]
            gps_type, gps_datas = gpsdatas.split(",", 1)

            # ignore $GPRMC 
            if gps_type != "$GPGGA":
                continue

            gps = pynmea2.parse(gpsdatas)
            self.simul_parsed_data.latitude  = float(gps.lat[:2]) + float(gps.lat[2:])/60
            self.simul_parsed_data.longitude = float(gps.lon[:3]) + float(gps.lat[3:])/60
            self.simul_parsed_data.altitude  = gps.altitude

    def get_data(self) :
        return self.simul_parsed_data

    def __del__(self):
        self.socket.close()
        print('del')
