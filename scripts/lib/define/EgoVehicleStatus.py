import ctypes

class EgoVehicleStatus(ctypes.Structure):
    _pack_ = 1 
    _fields_ = [
        ("header", ctypes.c_char * 11),
        ("data_lenght", ctypes.c_int),
        ("aux_data", ctypes.c_int * 3),
        ("sec", ctypes.c_float),
        ("nsec", ctypes.c_float),
        ("ctrl_mode", ctypes.c_byte),
        ("gear", ctypes.c_byte),
        ("signed_vel", ctypes.c_float),
        ("map_data_id", ctypes.c_int),
        ("accel", ctypes.c_float),
        ("brake", ctypes.c_float),
        ("size_x", ctypes.c_float),
        ("size_y", ctypes.c_float),
        ("size_z", ctypes.c_float),
        ("overhang", ctypes.c_float),
        ("wheelbase", ctypes.c_float),
        ("rear_overhang", ctypes.c_float),
        ("pos_x", ctypes.c_float),
        ("pos_y", ctypes.c_float),
        ("pos_z", ctypes.c_float),
        ("roll", ctypes.c_float),
        ("pitch", ctypes.c_float),
        ("yaw", ctypes.c_float),
        ("vel_x", ctypes.c_float),
        ("vel_y", ctypes.c_float),
        ("vel_z", ctypes.c_float),
        ("ang_vel_x", ctypes.c_float),
        ("ang_vel_y", ctypes.c_float),
        ("ang_vel_z", ctypes.c_float),
        ("accel_x", ctypes.c_float),
        ("accel_y", ctypes.c_float),
        ("accel_z", ctypes.c_float),
        ("steer", ctypes.c_float),
        ("link_id", ctypes.c_char * 38)      
    ]
