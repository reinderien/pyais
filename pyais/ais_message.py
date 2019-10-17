from pprint import pformat
from struct import unpack
from .constants import AISType
from .nmea_message import NMEAMessage
from .util import *


class AISMessage:
    """
    AIS message. Refer to
    https://en.wikipedia.org/wiki/Automatic_identification_system#Message_format
    https://gpsd.gitlab.io/gpsd/AIVDM.html
    """

    __slots__ = (
        'nmea',
        'ind',
        'attrs',
        'msg_type',
    )

    def __init__(self, nmea: NMEAMessage):
        self.nmea = nmea
        self.ind = 0
        self.attrs = {}

        if nmea.talker != 'AI' or nmea.msg_type not in ('VDM', 'VDO'):
            raise ValueError(f'"{nmea}" is not a supported AIS message')

        self.msg_type = AISType(self.eat(6))

    def eat(self, n: int) -> int:
        bits = self.nmea.bits[self.ind: self.ind + n]
        bits.fill()
        while len(bits) < 32:
            bits.frombytes(b'\0')
        (x,) = unpack('<I', bits.tobytes())
        self.ind += n
        return x

    def __str__(self):
        return f'{self.msg_type.name}: {pformat(self.attrs)}'





'''
def decode_msg_1(bit_vector):
    """
    AIS Vessel position report using SOTDMA (Self-Organizing Time Division Multiple Access)
    Src: https://gpsd.gitlab.io/gpsd/AIVDM.html#_types_1_2_and_3_position_report_class_a
    """
    status = to_int(bit_vector[38:42], 2)
    maneuver = to_int(bit_vector[143:145], 2)
    return {
        'type': to_int(bit_vector[0:6], 2),
        'repeat': to_int(bit_vector[6:8], 2),
        'mmsi': to_int(bit_vector[8:38], 2),
        'status': (status, NAVIGATION_STATUS.get(status, NULL)),
        'turn': signed(bit_vector[42:50]),
        'speed': to_int(bit_vector[50:60], 2),
        'accuracy': to_int(bit_vector[60], 2),
        'lon': signed(bit_vector[61:89]) / 600000.0,
        'lat': signed(bit_vector[89:116]) / 600000.0,
        'course': to_int(bit_vector[116:128], 2) * 0.1,
        'heading': to_int(bit_vector[128:137], 2),
        'second': to_int(bit_vector[137:143], 2),
        'maneuver': (maneuver, MANEUVER_INDICATOR.get(maneuver, NULL)),
        'raim': bool(to_int(bit_vector[148], 2)),
        'radio': to_int(bit_vector[149::], 2)
    }


def decode_msg_2(bit_vector):
    """AIS Vessel position report using SOTDMA (Self-Organizing Time Division Multiple Access)
    Src: https://gpsd.gitlab.io/gpsd/AIVDM.html#_types_1_2_and_3_position_report_class_a
    """
    return decode_msg_1(bit_vector)


def decode_msg_3(bit_vector):
    """
    AIS Vessel position report using ITDMA (Incremental Time Division Multiple Access)
    Src: https://gpsd.gitlab.io/gpsd/AIVDM.html#_types_1_2_and_3_position_report_class_a
    """
    return decode_msg_1(bit_vector)


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
