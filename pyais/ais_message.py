from enum import Enum
from importlib import import_module
from pprint import pformat
from .nmea_message import NMEAMessage, NMEAType


class AISGroup(Enum):
    # i.e. !AIVDO,1,1,,B,F000h>B2N2P3D73EB6`>6bT20000,0*75,runhtest,1172243748.04
    OWN_VESSEL = 'VDO'

    # i.e. !AIVDM,1,1,,A,33=HuF5000rsnlvHbvGt5b;:0000,0*29,rnhgb,1171830306.92
    OTHER_VESSEL = 'VDM'

    # i.e.
    # $AITXT,01,01,91,FREQ,2087,2088*57
    # $AITXT,01,01,50,AIS: GPS: no valid fix*4A
    INFO = 'TXT'

    # i.e. $AIALR,000000.00,002,V,V,AIS: Antenna VSWR exceeds limit*45,runhtest,1172243686.02
    ALARM = 'ALR'

    # https://yachtelectronics.blogspot.com/2011/02/srt-proprietary-ais-commands.html
    # i.e. $AISSD,@@@@@@@,@@@@@@@@@@@@@@@@@@@@,000,000,00,00,0,00*3C
    SHIP_STATIC_DATA = 'SSD'

    # https://yachtelectronics.blogspot.com/2011/02/srt-proprietary-ais-commands.html
    VESSEL_STATIC_DATA = 'VSD'

    # http://schwehr.org/blog/archives/2007-02.html
    # i.e. !AIBRF,0000012345,,0*43,runhtest,1172243745.36
    # Broadcast?? = 'BRF'

    # http://captainunlikely.com/blog/2015/07/10/under-the-hood-of-the-ais-600-transmitter/
    # i.e. $AIAIQ,VER*3C
    # ?? = 'AIQ'

    # http://captainunlikely.com/blog/2015/07/10/under-the-hood-of-the-ais-600-transmitter/
    # i.e. $AIVER,,,AI,GARMIN@,,9829,A038,G.2.14,05*36
    VERSION = 'VER'

    # https://fccid.io/CKEJHS-183/Test-Report/Test-Report-1-1846406
    # i.e. $AIACA,4,5200.0,N,00100.0,W,5000.0,N,00300.0,W,5,2084,0,2065,0,0,0,D,1,111840.00*3F
    # ?? = ACA


class AISType(Enum):
    # Refer to https://gpsd.gitlab.io/gpsd/AIVDM.html
    POS_CLASS_A1 = 1
    POS_CLASS_A2 = 2
    POS_CLASS_A3 = 3
    BASE_STATION = 4
    STATIC_AND_VOYAGE = 5
    BINARY_ADDRESSED = 6
    BINARY_ACK = 7
    BINARY_BROADCAST = 8
    SAR_AIRCRAFT_POS = 9
    DATE_INQ = 10
    DATE_RESP = 11
    SAFETY_MSG = 12
    SAFETY_ACK = 13
    SAFETY_BROADCAST = 14
    INTERROGATE = 15
    ASSIGN_MODE = 16
    DGNSS = 17
    POS_CLASS_B = 18
    POS_CLASS_B_EXT = 19
    LINK_MGMT = 20
    AID_TO_NAV = 21
    CHANNEL_MGMT = 22
    GROUP_ASSIGN = 23
    STATIC = 24
    BINARY_SINGLE_SLOT = 25
    BINARY_MULTI_SLOT = 26
    LONG_RANGE_BROADCAST = 27


class AISMessage:
    """
    AIS (Automatic Identification System) message. Refer to
    https://en.wikipedia.org/wiki/Automatic_identification_system#Message_format
    https://gpsd.gitlab.io/gpsd/AIVDM.html
    """

    __slots__ = (
        'nmea',
        'ind',
        'attrs',
        'group',
        'msg_type',
    )

    def __init__(self, nmea: NMEAMessage):
        self.nmea = nmea
        self.ind = 0
        self.attrs = {}

        if not self.is_ais(nmea):
            raise ValueError(f'"{nmea}" is not a supported AIS message')

        self.group = AISGroup(nmea.msg_type)
        if nmea.nmea_type == NMEAType.ENCAPSULATED and self.group in (
            AISGroup.OWN_VESSEL, AISGroup.OTHER_VESSEL
        ):
            self.msg_type = AISType(nmea.bits.uint(6))
            try:
                mod = import_module('pyais.ais.' + self.msg_type.name.lower())
                self.attrs = mod.decode(nmea.bits)
            except ModuleNotFoundError:
                pass
        else:
            self.msg_type = None

    @staticmethod
    def is_ais(nmea: NMEAMessage) -> bool:
        return nmea.talker == 'AI'

    def __str__(self):
        if self.msg_type:
            return f'{self.group.name}/{self.msg_type.name}: {self.attrs}'
        return f'{self.group.name} unsupported: {self.nmea.raw}'
