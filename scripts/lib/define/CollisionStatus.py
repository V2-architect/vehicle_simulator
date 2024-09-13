import ctypes

class CollisionStatus(ctypes.Structure):
    _pack_ = 1 
    _fields_ = [
        ("header", ctypes.c_char * 15),
        ("data_lenght", ctypes.c_int),
        ("aux_data", ctypes.c_int * 3),
        ("timestamp(total)", ctypes.c_int),
        ("timestamp(nano)",  ctypes.c_int),

        ("obj_type_01", ctypes.c_short),
        ("obj_id_01", ctypes.c_short),
        ("pos_x_01", ctypes.c_int),
        ("pos_y_01", ctypes.c_int),
        ("pos_z_01", ctypes.c_int),
        ("global_offset_x_01", ctypes.c_int),
        ("global_offset_y_01", ctypes.c_int),
        ("global_offset_z_01", ctypes.c_int),

        ("obj_type_02", ctypes.c_short),
        ("obj_id_02", ctypes.c_short),
        ("pos_x_02", ctypes.c_int),
        ("pos_y_02", ctypes.c_int),
        ("pos_z_02", ctypes.c_int),
        ("global_offset_x_02", ctypes.c_int),
        ("global_offset_y_02", ctypes.c_int),
        ("global_offset_z_02", ctypes.c_int)

    ]
