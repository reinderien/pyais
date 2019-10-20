from datetime import datetime, timedelta
from enum import Enum
from ..bits import Bits


# https://www.navcen.uscg.gov/?pageName=AISMessagesA


class NavigationStatus(Enum):
    USING_ENGINE                = 0
    AT_ANCHOR                   = 1
    NOT_UNDER_COMMAND           = 2
    RESTRICTED_MANOEUVERABILITY = 3
    CONSTRAINED_BY_DRAUGHT      = 4
    MOORED                      = 5
    AGROUND                     = 6
    FISHING                     = 7
    SAILING                     = 8
    NAV_HIGHSPEED               = 9
    NAV_WING_IN_GND             = 10
    POWERED_TOW_ASTERN          = 11
    POWERED_PUSH                = 12
    RESERVED_13                 = 13
    AIS_SART                    = 14
    UNDEFINED                   = 15


class TimeMode(Enum):
    EPFS         = 0
    UNAVAILABLE  = 60
    MANUAL_INPUT = 61
    ESTIMATED    = 62
    INOPERATIVE  = 63


class SpecialManoeuvreStatus(Enum):
    UNAVAILABLE = 0
    NOT_ENGAGED = 1
    ENGAGED     = 2


class SyncState(Enum):
    UTC_DIRECT    = 0
    UTC_INDIRECT  = 1
    BASE_DIRECT   = 2
    BASE_INDIRECT = 3


def decode_turn(turn: int) -> (bool, float, float):
    # turn_indicate_avail, turn_min_dps, turn_max_dps
    if turn == -128:
        return False, None, None
    if turn == -127:
        return False, float('-inf'), -5/30
    if turn < 0:
        # ROTAIS = 4.733 SQRT(ROTsensor) °/min
        sens = -(turn/4.733)**2 / 60
        return True, sens, sens
    if turn < 127:
        sens = (turn/4.733)**2 / 60
        return True, sens, sens
    if turn == 127:
        return False, 5/30, float('inf')
    raise ValueError()


def decode_pos(pos: int, undef: int) -> float:
    # pos is in 1/10000 minutes
    # 1° = 60m
    degrees = pos / 10_000 / 60
    if degrees == undef:
        return None
    # assert -undef < degrees < undef
    return degrees


def decode_course(course: int) -> float:
    if course == 3600:
        return None
    # assert 0 <= course < 3600
    return course / 10


def decode_heading(head: int) -> float:
    if head == 511:
        return None
    # assert 0 <= head < 360
    return head


def decode_time(second: int) -> (TimeMode, datetime):
    if second >= 60:
        return TimeMode(second), None

    # Let's hope that your clock is synchronized
    now = datetime.utcnow()
    subst = now.replace(second=second, microsecond=0)
    delta = (subst - now).total_seconds()
    if delta > 30:
        subst -= timedelta(minutes=1)
    elif delta < -30:
        subst += timedelta(minutes=1)
    return TimeMode.EPFS, subst


def decode(bits: Bits) -> dict:
    d = {
        'repeat': bits.uint(2),
        'mmsi': bits.uint(30),
        'status': NavigationStatus(bits.uint(4)),
    }

    turn = bits.int(8)
    ti_avail, turn_min, turn_max = decode_turn(turn)

    d.update({
        'turn_indicate_avail': ti_avail,
        'turn_min_dps': turn_min,
        'turn_max_dps': turn_max,

        'speed_knots': bits.uint(10)/10,
        'accuracy_sub_10m': bits.bool(),
        'long_deg': decode_pos(bits.int(28), 181),
        'lat_deg': decode_pos(bits.int(27), 91),
        'course_deg': decode_course(bits.uint(12)),
        'heading_deg': decode_heading(bits.uint(9)),

        'time': decode_time(bits.uint(6)),
        'special_manoeuvre': SpecialManoeuvreStatus(bits.uint(2)),
        'spare': bits.raw(3),
        'raim_in_use': bits.bool(),

        'sync': SyncState(bits.uint(2)),
        'slot_timeout': bits.uint(3),
        # Described in https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1371-5-201402-I!!PDF-E.pdf ?
        'comm_state': bits.raw(14)
    })

    bits.end()
    return d
