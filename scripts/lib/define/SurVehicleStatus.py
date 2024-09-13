import ctypes

class SurVehicleStatus(ctypes.Structure):
    _pack_ = 1 
    _fields_ = [
        ("header", ctypes.c_char * 14),
        ("data_lenght", ctypes.c_int),
        ("aux_data", ctypes.c_int * 3),
        ("timestamp(total)", ctypes.c_int),
        ("timestamp(nano)",  ctypes.c_int),
        ("obj_id", ctypes.c_short),
        ("obj_type", ctypes.c_short),
        ("pos_x", ctypes.c_int),
        ("pos_y", ctypes.c_int),
        ("pos_z", ctypes.c_int),
        ("heading", ctypes.c_int),
        ("size_x", ctypes.c_int),
        ("size_y", ctypes.c_int),
        ("size_z", ctypes.c_int),
        ("overhang", ctypes.c_float),
        ("wheelbase", ctypes.c_float),
        ("rear_overhang", ctypes.c_float),
        ("vel_x", ctypes.c_float),
        ("vel_y", ctypes.c_float),
        ("vel_z", ctypes.c_float),
        ("accel_x", ctypes.c_float),
        ("accel_y", ctypes.c_float),
        ("accel_z", ctypes.c_float),
        ("link_id", ctypes.c_char * 38)      
    ]
