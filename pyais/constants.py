from enum import Enum

# Keywords
UNDEFINED = 'Undefined'
RESERVED = 'Reserved'
NULL = 'N/A'


class NMEAType(Enum):
    COMMENT = '#'
    DELIMITED = '$'
    ENCAPSULATED = '!'


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


NAVIGATION_STATUS = {
    0: 'Under way using engine',
    1: 'At anchor',
    2: 'Not under command',
    3: 'Restricted manoeuverability',
    4: 'Constrained by her draught',
    5: 'Moored',
    6: 'Aground',
    7: 'Engaged in Fishing',
    8: 'Under way sailing',
    9: 'Reserved',
    10: 'Reserved',
    11: 'Reserved',
    12: 'Reserved',
    13: 'Reserved',
    14: 'AIS-SART is active',
    15: 'Undefined',
}

MANEUVER_INDICATOR = {
    0: 'Not available',
    1: 'No special maneuver',
    2: 'Special maneuver'
}

EPFD_TYPE = {
    0: 'Undefined',
    1: 'GPS',
    2: 'GLONASS',
    3: 'GPS/GLONASS',
    4: 'Loran-C',
    5: 'Chayka',
    6: 'Integrated navigation system',
    7: 'Surveyed',
    8: 'Galileo',
    15: 'Undefined'
}

SHIP_TYPE = {
    0: 'Not available',
    20: 'Wing in ground (WIG)',
    21: 'Wing in ground (WIG), Hazardous category A',
    22: 'Wing in ground (WIG), Hazardous category B',
    23: 'Wing in ground (WIG), Hazardous category C',
    24: 'Wing in ground (WIG), Hazardous category D',
    25: 'WIG Reserved',
    26: 'WIG Reserved',
    27: 'WIG Reserved',
    28: 'WIG Reserved',
    29: 'WIG Reserved',
    30: 'Fishing',
    31: 'Towing',
    32: 'Towing,length exceeds 200m or breadth exceeds 25m',
    33: 'Dredging or underwater ops',
    34: 'Diving ops',
    35: 'Military ops',
    36: 'Sailing',
    37: 'Pleasure Craft',
    38: 'Reserved',
    39: 'Reserved',
    40: 'High speed craft (HSC)',
    41: 'High speed craft (HSC), Hazardous category A',
    42: 'High speed craft (HSC), Hazardous category B',
    43: 'High speed craft (HSC), Hazardous category C',
    44: 'High speed craft (HSC), Hazardous category D',
    45: 'High speed craft (HSC), Reserved',
    46: 'High speed craft (HSC), Reserved',
    47: 'High speed craft (HSC), Reserved',
    48: 'High speed craft (HSC), Reserved',
    49: 'High speed craft (HSC), No additional information',
    50: 'Pilot Vessel',
    51: 'Search and Rescue vessel',
    52: 'Tug',
    53: 'Port Tender',
    54: 'Anti-pollution equipment',
    55: 'Law Enforcement',
    56: 'Spare - Local Vessel',
    57: 'Spare - Local Vessel',
    58: 'Medical Transport',
    59: 'Noncombatant ship according to RR Resolution No. 18',
    60: 'Passenger',
    61: 'Passenger, Hazardous category A',
    62: 'Passenger, Hazardous category B',
    63: 'Passenger, Hazardous category C',
    64: 'Passenger, Hazardous category D',
    65: 'Passenger, Reserved',
    66: 'Passenger, Reserved',
    67: 'Passenger, Reserved',
    68: 'Passenger, Reserved',
    69: 'Passenger, No additional information',
    70: 'Cargo',
    71: 'Cargo, Hazardous category A',
    72: 'Cargo, Hazardous category B',
    73: 'Cargo, Hazardous category C',
    74: 'Cargo, Hazardous category D',
    75: 'Cargo, Reserved',
    76: 'Cargo, Reserved',
    77: 'Cargo, Reserved',
    78: 'Cargo, Reserved',
    79: 'Cargo, No additional information',
    80: 'Tanker',
    81: 'Tanker, Hazardous category A',
    82: 'Tanker, Hazardous category B',
    83: 'Tanker, Hazardous category C',
    84: 'Tanker, Hazardous category D',
    85: 'Tanker, Reserved ',
    86: 'Tanker, Reserved ',
    87: 'Tanker, Reserved ',
    88: 'Tanker, Reserved ',
    89: 'Tanker, No additional information',
    90: 'Other Type',
    91: 'Other Type, Hazardous category A',
    92: 'Other Type, Hazardous category B',
    93: 'Other Type, Hazardous category C',
    94: 'Other Type, Hazardous category D',
    95: 'Other Type, Reserved',
    96: 'Other Type, Reserved',
    97: 'Other Type, Reserved',
    98: 'Other Type, Reserved',
    99: 'Other Type, No additional information'
}

DAC_FID = {
    '1-12': 'Dangerous cargo indication',
    '1-14': 'Tidal window',
    '1-16': 'Number of persons on board',
    '1-18': 'Clearance time to enter port',
    '1-20': 'Berthing data (addressed)',
    '1-23': 'Area notice (addressed)',
    '1-25': 'Dangerous Cargo indication',
    '1-28': 'Route info addressed',
    '1-30': 'Text description addressed',
    '1-32': 'Tidal Window',
    '200-21': 'ETA at lock/bridge/terminal',
    '200-22': 'RTA at lock/bridge/terminal',
    '200-55': 'Number of persons on board',
    '235-10': 'AtoN monitoring data (UK)',
    '250-10': 'AtoN monitoring data (ROI)',
}

