from ..bits import Bits


def decode(bits: Bits) -> dict:
    return {}

'''
def decode_msg_4(bit_vector):
    """
    AIS Vessel position report using SOTDMA (Self-Organizing Time Division Multiple Access)
    Src: https://gpsd.gitlab.io/gpsd/AIVDM.html#_type_4_base_station_report
    """
    epfd = to_int(bit_vector[134:138], 2)
    return {
        'type': to_int(bit_vector[0:6], 2),
        'repeat': to_int(bit_vector[6:8], 2),
        'mmsi': to_int(bit_vector[8:38], 2),
        'year': to_int(bit_vector[38:52], 2),
        'month': to_int(bit_vector[52:56]),
        'day': to_int(bit_vector[56:61], 2),
        'hour': to_int(bit_vector[61:66], 2),
        'minute': to_int(bit_vector[66:72], 2),
        'second': to_int(bit_vector[72:78], 2),
        'accuracy': bool(to_int(bit_vector[78], 2)),
        'lon': signed(bit_vector[66:72]) / 600000.0,
        'lat': signed(bit_vector[66:72]) / 600000.0,
        'epfd': (epfd, EPFD_TYPE.get(epfd, NULL)),
        'raim': bool(to_int(bit_vector[148], 2)),
        'radio': to_int(bit_vector[148::], 2)
    }
'''
