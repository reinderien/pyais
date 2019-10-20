from . import pos_class_a1
from ..bits import Bits


def decode(bits: Bits) -> dict:
    return pos_class_a1.decode(bits)
