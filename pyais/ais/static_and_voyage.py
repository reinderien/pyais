from ..bits import Bits


def decode(bits: Bits) -> dict:
    return {}


'''
def decode_msg_5(bit_vector):
    epfd = to_int(bit_vector[270:274], 2)
    ship_type = to_int(bit_vector[66:72], 2)
    return {
        'type': to_int(bit_vector[0:6], 2),
        'repeat': to_int(bit_vector[6:8], 2),
        'mmsi': to_int(bit_vector[8:38], 2),
        'ais_version': to_int(bit_vector[38:40], 2),
        'imo': to_int(bit_vector[40:70], 2),
        'callsign': bin_to_ascii6(bit_vector[70:112]),
        'shipname': bin_to_ascii6(bit_vector[112:232]),
        'shiptype': (ship_type, SHIP_TYPE.get(ship_type, NULL)),
        'to_bow': to_int(bit_vector[240:249], 2),
        'to_stern': to_int(bit_vector[249:258], 2),
        'to_port': to_int(bit_vector[258:264], 2),
        'to_starboard': to_int(bit_vector[264:270], 2),
        'epfd': (epfd, EPFD_TYPE.get(epfd, NULL)),
        'month': to_int(bit_vector[274:278], 2),
        'day': to_int(bit_vector[278:283], 2),
        'hour': to_int(bit_vector[283:288], 2),
        'minute': to_int(bit_vector[288:294], 2),
        'draught': to_int(bit_vector[294:302], 2) / 10.0,
        'destination': bin_to_ascii6(bit_vector[302::])
    }
'''
