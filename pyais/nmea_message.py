from .constants import NMEAType
from bitarray import bitarray
from functools import reduce
from operator import xor
from typing import Sequence


class NMEAMessage:
    """
    NMEA0183 message. Refer to
    https://en.wikipedia.org/wiki/NMEA_0183
    """

    __slots__ = (
        'raw',
        'bits',
        'nmea_type',
        'talker',
        'msg_type',
        'sentence_count',
        'sentence_index',
        'seq_id',
        'channel',
        'data',
    )

    STRICT = True

    def __init__(self, raw: str):
        self.raw = raw
        self.bits: bitarray = None
        self.nmea_type = NMEAType(raw[0])
        if self.nmea_type != NMEAType.ENCAPSULATED:
            return  # silently give up - this is not invalid but we don't support it

        (
            msg_type,
            sentence_count,
            sentence_index,
            seq_id,
            channel,
            data,
            checksum,
        ) = raw.split(',')

        self.talker = msg_type[1:3]
        self.msg_type = msg_type[3:]
        self.sentence_count = int(sentence_count)
        self.sentence_index = int(sentence_index)
        self.seq_id = seq_id
        self.channel = channel
        self.data = data

        self._verify(checksum)

    def _verify(self, checksum: str):
        # Not actually true
        # assert checksum[:2] == '0*'

        checked = (ord(c) for c in self.raw[1:].split('*', 1)[0])
        actual = reduce(xor, checked)
        expected = int(checksum[2:], 16)
        assert actual == expected

        assert 1 <= self.sentence_index <= self.sentence_count

        if self.STRICT:
            assert self.channel in ('A', 'B')
            assert not ((self.sentence_count > 1) ^
                        bool(self.seq_id))

    @staticmethod
    def _char_to_bin(c: str) -> int:
        c = ord(c)

        if 0x30 <= c <= 0x57:
            c -= 0x30
        elif 0x60 <= c <= 0x77:
            c -= 0x38
        else:
            raise ValueError(f'Invalid data character {c}')

        return c

    @classmethod
    def reduce(cls, messages: Sequence):
        bits = bitarray(endian='little')

        for msg in messages:
            for c in msg.data:
                bits.frombytes(bytes((cls._char_to_bin(c),)))
                bits.pop()
                bits.pop()

        messages[0].bits = bits
        return messages[0]

    def follows(self, prev) -> bool:
        return (
            self.nmea_type == prev.nmea_type
            and self.msg_type == prev.msg_type
            and self.talker == prev.talker
            and self.channel == prev.channel
            and self.seq_id == prev.seq_id
            and self.sentence_count == prev.sentence_count
            and self.sentence_index == prev.sentence_index + 1
        )

    def single(self) -> bool:
        return (
            not self.seq_id
            and self.sentence_index == 1
            and self.sentence_count == 1
        )

    def multi(self) -> bool:
        return (
            self.seq_id
            and self.sentence_count > 1
        )

    def __str__(self):
        return self.raw
