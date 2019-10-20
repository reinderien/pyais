from ..bits import Bits


def decode(bits: Bits) -> dict:
    return {}


'''
def decode_msg_8(bit_vector):
    """
    Binary Broadcast Message
    TODO: data needs to be interpreted depending DAC-FID
    """
    return {
        'type': to_int(bit_vector[0:6], 2),
        'repeat': to_int(bit_vector[6:8], 2),
        'mmsi': to_int(bit_vector[8:38], 2),
        'dac': to_int(bit_vector[40:50], 2),
        'fid': to_int(bit_vector[50:56], 2),
        'data': to_int(bit_vector[56::], 2),
    }
'''
