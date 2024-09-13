import ctypes

class TrafficLightStatus(ctypes.Structure):
    _pack_ = 1 
    _fields_ = [
        ("header", ctypes.c_char * 14),
        ("data_lenght", ctypes.c_int),
        ("aux_data", ctypes.c_int * 3),
        ("traffic_light_index", ctypes.c_char*12),
        ("traffic_light_type", ctypes.c_short),
        ("traffic_light_status", ctypes.c_short)
    ]
