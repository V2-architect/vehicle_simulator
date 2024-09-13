import time
import ctypes
import os
import pdb
import threading
import socket
import struct

from lib.define.EgoVehicleStatus import EgoVehicleStatus
from lib.define.SurVehicleStatus import SurVehicleStatus
from lib.define.CollisionStatus import CollisionStatus
from lib.define.TrafficLightStatus import TrafficLightStatus
from lib.define.IntersectionStatus import IntersectionStatus
from lib.define.GPSStatus import GPSStatus

from lib.simul_connector import SimulData
from lib.simul_connector import SimulDataHandler
from lib import network_setting as simul_net


import logging
logging.basicConfig(level=logging.INFO, format='[VSimul][%(asctime)s] %(message)s', datefmt='%y%m%d-%H%M%S')


def start_simul_data_handlers():
    IP = simul_net.SimulDataDstIp

    # simul data handler threads
    ego_vehicle_handler   = SimulDataHandler(IP, simul_net.PORT_info['EgoVehicleStatus'], EgoVehicleStatus())
    collision_handler     = SimulDataHandler(IP, simul_net.PORT_info['CollisionInfo'], CollisionStatus())
    intersection_handler  = SimulDataHandler(IP, simul_net.PORT_info['IntersectionInfo'], IntersectionStatus())
    sur_vehicle_handler   = SimulDataHandler(IP, simul_net.PORT_info['SurVehicleStatus'], SurVehicleStatus())
    traffic_light_handler = SimulDataHandler(IP, simul_net.PORT_info['TrafficLightInfo'], TrafficLightStatus())
    gps_handler           = SimulDataHandler(IP, simul_net.PORT_info['GPSStatus'], GPSStatus())

    return {
        "ego_vehicle": ego_vehicle_handler,
        "collision": collision_handler,
        "intersection": intersection_handler,
        "sur_vehicle": sur_vehicle_handler,
        "traffic_light": traffic_light_handler,
        "gps": gps_handler,
    }

def update_ego_vehicle(handler, simul_data):
    while True:
        data = handler.get_data()
        simul_data.vehicle_speed_x = data.vel_x
        simul_data.vehicle_speed_y = data.vel_y
        simul_data.vehicle_speed_z = data.vel_z
        simul_data.vehicle_roll = data.roll
        simul_data.vehicle_pitch = data.pitch
        simul_data.vehicle_yaw = data.yaw
        simul_data.angular_velocity_x = data.ang_vel_x
        simul_data.angular_velocity_y = data.ang_vel_y
        simul_data.angular_velocity_z = data.ang_vel_z
        simul_data.accel_x = data.accel_x
        simul_data.accel_y = data.accel_y
        simul_data.accel_z = data.accel_z
        simul_data.gear = data.gear
        simul_data.accel_pressure = data.accel
        simul_data.brake_pressure = data.brake
        simul_data.steerwheel_deg = data.steer

        #logging.info("[EgoVehicle] update simul data")
        time.sleep(0.01)

def update_sur_vehicle(handler, simul_data):
    while True:
        data = handler.get_data()
        simul_data.object_type = data.obj_type
        simul_data.object_velocity_x = data.vel_x
        simul_data.object_velocity_y = data.vel_y
        simul_data.object_velocity_z = data.vel_z
        simul_data.object_accel_x = data.accel_x
        simul_data.object_accel_y = data.accel_y
        simul_data.object_accel_z = data.accel_z

        #logging.info("[SurVehicle] update simul data")
        time.sleep(0.01)

def update_collision(handler, simul_data):
    while True:
        data = handler.get_data()
        # expand object_type_02, 03, 04 ?
        simul_data.collision_object_type = data.obj_type_01

        #logging.info("[Collision] update simul data")
        time.sleep(0.01)

def update_traffic_light(handler, simul_data):
    while True:
        data = handler.get_data()
        simul_data.traffic_light_type = data.traffic_light_type
        simul_data.traffic_light_status = data.traffic_light_status

        #logging.info("[Traffic] update simul data")
        time.sleep(0.01)

def update_intersection(handler, simul_data):
    while True:
        data = handler.get_data()
        simul_data.intersection_index = data.intersection_index
        simul_data.intersection_status = data.intersection_status
        simul_data.intersection_time = data.intersection_time

        #logging.info("[Intersection] update simul data")
        time.sleep(0.01)

def update_gps(handler, simul_data):
    while True:
        data = handler.get_data()
        simul_data.latitude = data.latitude
        simul_data.longitude = data.longitude
        simul_data.altitude = data.altitude

        #logging.info("[GPS] update simul data")
        time.sleep(0.01)


def start_update_data_handlers(data_handlers, simul_data):
    ego_vehicle_update_handler = threading.Thread(target=update_ego_vehicle, args=(data_handlers['ego_vehicle'], simul_data))
    collision_update_handler = threading.Thread(target=update_collision, args=(data_handlers['collision'], simul_data))
    intersection_update_handler = threading.Thread(target=update_intersection, args=(data_handlers['intersection'], simul_data))
    sur_vehicle_update_handler = threading.Thread(target=update_sur_vehicle, args=(data_handlers['sur_vehicle'], simul_data))
    traffic_light_update_handler = threading.Thread(target=update_traffic_light, args=(data_handlers['traffic_light'], simul_data))
    gps_update_handler = threading.Thread(target=update_gps, args=(data_handlers['gps'], simul_data))

    handlers = [
        ego_vehicle_update_handler,
        collision_update_handler,
        intersection_update_handler,
        sur_vehicle_update_handler,
        traffic_light_update_handler,
        gps_update_handler
    ]
    return handlers

def show_simul_data(simul_data):
    while True:
        #logging.info(f"vel_x: {simul_data.vehicle_speed_x}")
        #logging.info(f"vel_y: {simul_data.vehicle_speed_y}")
        #logging.info(f"vel_z: {simul_data.vehicle_speed_z}")

        logging.info(f"gear: {simul_data.gear}")
        logging.info(f"accel_pressure: {simul_data.accel_pressure}")
        logging.info(f"brake_pressure: {simul_data.brake_pressure}")
        logging.info("=" * 50)
        time.sleep(0.2)



class DataPublisher:
    def __init__(self, name, socket_path, simul_data, get_packed_data, delay=1):
        self.thread_name = name
        self.socket_path = socket_path
        self.simul_data = simul_data
        self.get_packed_data = get_packed_data
        self.delay = delay

    def start(self):
        while True:
            if os.path.exists(self.socket_path):
                try:
                    # 소켓 생성
                    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                    client_socket.connect(self.socket_path)
                    logging.info(f"[{self.thread_name}] Connected to server")

                    while True:
                        try:
                            # [2] ===================================================
                            packed_data = self.get_packed_data(self.simul_data)
                            # [2] ===================================================

                            client_socket.sendall(packed_data)
                            #client_socket.sendall(str(counter).encode('utf-8'))
                            #logging.info(f"Sent: {data}")

                            # [3] ===================================================
                            time.sleep(self.delay)
                            # [3] ===================================================
                        except socket.error:
                            logging.info(f"[{self.thread_name}] Server closed the connection")
                            break
                    client_socket.close()
                except socket.error:
                    logging.info(f"[{self.thread_name}] Failed to connect to server")
            else:
                logging.info(f"[{self.thread_name}] Waiting for server to open the socket")
            time.sleep(self.delay)



def provide_vehicle_speed(th_name, simul_data):
    socket_path = "/home/jhshin/work/someip_app/tmp/uds_vehicle_speed"

    def get_packed_data(simul_data):
        data = (simul_data.vehicle_speed_x,
                simul_data.vehicle_speed_y,
                simul_data.vehicle_speed_z)
        packed_data = struct.pack('fff', *data)
        return packed_data

    publisher = DataPublisher(th_name, socket_path, simul_data, get_packed_data)
    publisher.start()


def provide_vehicle_pose(th_name, simul_data):
    socket_path = "/home/jhshin/work/morai/uds_vehicle_pose"

    def get_packed_data(simul_data):
        data = (simul_data.vehicle_roll,
                simul_data.vehicle_pitch,
                simul_data.vehicle_yaw,
                simul_data.angular_velocity_x,
                simul_data.angular_velocity_y,
                simul_data.angular_velocity_z)
        packed_data = struct.pack('ffffff', *data)
        return packed_data

    publisher = DataPublisher(th_name, socket_path, simul_data, get_packed_data)
    publisher.start()

def provide_vehicle_accel(th_name, simul_data):
    socket_path = "/home/jhshin/work/morai/uds_vehicle_accel"

    def get_packed_data(simul_data):
        data = (simul_data.accel_x,
                simul_data.accel_y,
                simul_data.accel_z)
        packed_data = struct.pack('fff', *data)
        return packed_data

    publisher = DataPublisher(th_name, socket_path, simul_data, get_packed_data)
    publisher.start()

def provide_transmission(th_name, simul_data):
    socket_path = "/home/jhshin/work/morai/uds_transmission"

    def get_packed_data(simul_data):
        data = (simul_data.gear,)
        packed_data = struct.pack('i', *data)
        return packed_data

    publisher = DataPublisher(th_name, socket_path, simul_data, get_packed_data)
    publisher.start()

def provide_driving(th_name, simul_data):
    socket_path = "/home/jhshin/work/morai/uds_driving"

    def get_packed_data(simul_data):
        data = (simul_data.accel_pressure,
                simul_data.brake_pressure)
        packed_data = struct.pack('ff', *data)
        return packed_data

    publisher = DataPublisher(th_name, socket_path, simul_data, get_packed_data)
    publisher.start()

def provide_steeringwheel(th_name, simul_data):
    socket_path = "/home/jhshin/work/morai/uds_steeringwheel"

    def get_packed_data(simul_data):
        data = (simul_data.steerwheel_deg,)
        packed_data = struct.pack('f', *data)
        return packed_data

    publisher = DataPublisher(th_name, socket_path, simul_data, get_packed_data)
    publisher.start()

def provide_object_detection(th_name, simul_data):
    socket_path = "/home/jhshin/work/morai/uds_object_detection"

    def get_packed_data(simul_data):
        data = (simul_data.object_type,
                simul_data.object_velocity_x,
                simul_data.object_velocity_y,
                simul_data.object_velocity_z,
                simul_data.object_accel_x,
                simul_data.object_accel_y,
                simul_data.object_accel_z)
        packed_data = struct.pack('iffffff', *data)
        return packed_data

    publisher = DataPublisher(th_name, socket_path, simul_data, get_packed_data)
    publisher.start()

def provide_collision(th_name, simul_data):
    socket_path = "/home/jhshin/work/morai/uds_collision"

    def get_packed_data(simul_data):
        data = (simul_data.object_type,)
        packed_data = struct.pack('i', *data)
        return packed_data

    publisher = DataPublisher(th_name, socket_path, simul_data, get_packed_data)
    publisher.start()


def provide_traffic_light(th_name, simul_data):
    socket_path = "/home/jhshin/work/morai/uds_traffic_light"

    def get_packed_data(simul_data):
        data = (simul_data.traffic_light_type,
                simul_data.traffic_light_status)

        packed_data = struct.pack('ii', *data)
        return packed_data

    publisher = DataPublisher(th_name, socket_path, simul_data, get_packed_data)
    publisher.start()


def provide_intersection(th_name, simul_data):
    socket_path = "/home/jhshin/work/morai/uds_intersection"

    def get_packed_data(simul_data):
        data = (simul_data.intersection_index,
                simul_data.intersection_status,
                simul_data.intersection_time)

        packed_data = struct.pack('iif', *data)
        return packed_data

    publisher = DataPublisher(th_name, socket_path, simul_data, get_packed_data)
    publisher.start()


def provide_location(th_name, simul_data):
    socket_path = "/home/jhshin/work/morai/uds_location"

    def get_packed_data(simul_data):
        data = (simul_data.latitude,
                simul_data.longitude,
                simul_data.altitude)

        packed_data = struct.pack('fff', *data)
        return packed_data

    publisher = DataPublisher(th_name, socket_path, simul_data, get_packed_data, 1)
    publisher.start()


def start_data_providing_handlers(simul_data):
    vehicle_speed_provider_handler = threading.Thread(target=provide_vehicle_speed, args=("VehicleSpeed", simul_data,))
    vehicle_pose_provider_handler = threading.Thread(target=provide_vehicle_pose, args=("VehiclePose", simul_data,))
    vehicle_accel_provider_handler = threading.Thread(target=provide_vehicle_accel, args=("VehicleAccel", simul_data,))
    transmission_provider_handler = threading.Thread(target=provide_transmission, args=("Transmission", simul_data,))
    driving_provider_handler = threading.Thread(target=provide_driving, args=("Driving", simul_data,))
    steeringwheel_provider_handler = threading.Thread(target=provide_steeringwheel, args=("SteeringWheel", simul_data,))
    object_detection_provider_handler = threading.Thread(target=provide_object_detection, args=("ObjectDetection", simul_data,))
    collision_provider_handler = threading.Thread(target=provide_collision, args=("Collision", simul_data,))
    traffic_light_provider_handler = threading.Thread(target=provide_traffic_light, args=("TrafficLight", simul_data,))
    intersection_provider_handler = threading.Thread(target=provide_intersection, args=("Intersection", simul_data,))
    location_provider_handler = threading.Thread(target=provide_location, args=("Location", simul_data,))

    handlers = [
        vehicle_speed_provider_handler,
        vehicle_pose_provider_handler,
        vehicle_accel_provider_handler,
        transmission_provider_handler,
        driving_provider_handler,
        steeringwheel_provider_handler,
        object_detection_provider_handler,
        collision_provider_handler,
        traffic_light_provider_handler,
        intersection_provider_handler,
        location_provider_handler
    ]

    return handlers


def main():
    # common instance for all threads
    simul_data = SimulData()

    logging.info("[1] start receiving simul data handlers")
    data_handlers   = start_simul_data_handlers()

    logging.info("[2] start updating data handlers")
    update_handlers = start_update_data_handlers(data_handlers, simul_data)
    for handler in update_handlers:
        handler.start()

    #debug_th = threading.Thread(target=show_simul_data, args=(simul_data,)).start()
    #update_handlers.append(debug_th)

    logging.info("[3] start data provideing to SOME/IP services handlers")
    data_providing_handlers = start_data_providing_handlers(simul_data)
    for handler in data_providing_handlers:
        handler.start()

    logging.info("wait at the main thread")
    for handler in update_handlers:
        handler.join()


if __name__ == '__main__':
    main()
