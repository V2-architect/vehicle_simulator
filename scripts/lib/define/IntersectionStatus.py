import ctypes

class IntersectionStatus(ctypes.Structure):
    _pack_ = 1 
    _fields_ = [
        ("header", ctypes.c_char * 11),
        ("data_lenght", ctypes.c_int),
        ("aux_data", ctypes.c_int * 3),
        ("intersection_index", ctypes.c_short),
        ("intersection_status", ctypes.c_short),
        ("intersection_time", ctypes.c_float)
    ]
