from ..bits import Bits


def decode(bits: Bits) -> dict:
    return {}


'''
def decode_msg_18(bit_vector):
    """
    Standard Class B CS Position Report
    Src: https://gpsd.gitlab.io/gpsd/AIVDM.html#_type_18_standard_class_b_cs_position_report
    """
    return {
        'type': to_int(bit_vector[0:6], 2),
        'repeat': to_int(bit_vector[6:8], 2),
        'mmsi': to_int(bit_vector[8:38], 2),
        'speed': to_int(bit_vector[46:55], 2),
        'accuracy': bool(to_int(bit_vector[55], 2)),
        'lon': signed(bit_vector[56:85]) / 600000.0,
        'lat': signed(bit_vector[85:112]) / 600000.0,
        'course': to_int(bit_vector[112:124], 2) * 0.1,
        'heading': to_int(bit_vector[124:133], 2),
        'second': to_int(bit_vector[133:139], 2),
        'regional': to_int(bit_vector[139:141], 2),
        'cs': bool(to_int(bit_vector[141])),
        'display': bool(to_int(bit_vector[142])),
        'dsc': bool(to_int(bit_vector[143])),
        'band': bool(to_int(bit_vector[144])),
        'msg22': bool(to_int(bit_vector[145])),
        'assigned': bool(to_int(bit_vector[146])),
        'raim': bool(to_int(bit_vector[147])),
        'radio': to_int(bit_vector[148::]),
    }
'''
