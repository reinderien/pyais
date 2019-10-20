from struct import unpack

from bitarray import bitarray


class Bits:
    """
    bitarray is missing some features, and bitstring is fundamentally broken
    when it comes to LSB bit ordering.
    """

    def __init__(self, ascii6: str):
        self.bits = bitarray(endian='little')
        self.read_at = 0

        for a in ascii6:
            byte = self.char_to_bin(a)
            self.bits.frombytes(bytes((byte,)))
            self.bits.pop()
            self.bits.pop()

    @staticmethod
    def char_to_bin(c: str) -> int:
        c = ord(c)

        if 0x30 <= c <= 0x57:
            c -= 0x30
        elif 0x60 <= c <= 0x77:
            c -= 0x38
        else:
            raise ValueError(f'Invalid data character {c}')

        return c

    def uint(self, n: int) -> int:
        if n > 32:
            raise NotImplementedError()

        bits = self.raw(n)
        bits.fill()
        while len(bits) < 32:
            bits.frombytes(b'\0')
        (x,) = unpack('<I', bits.tobytes())
        return x

    def int(self, n: int) -> int:
        x = self.uint(n)
        if x >= 1 << (n-1):
            x -= 1 << n
        return x

    def bool(self) -> bool:
        x = self.bits[self.read_at]
        self.read_at += 1
        return x

    def raw(self, n: int) -> bitarray:
        x = self.bits[self.read_at: self.read_at + n]
        self.read_at += n
        return x

    def end(self):
        slack = len(self.bits) - self.read_at
        if slack != 0:
            raise ValueError(f'{slack} bits left after decoding')
