from traceback import print_exc
from typing import Iterator

from .ais_message import AISMessage
from .constants import NMEAType
from .nmea_message import NMEAMessage
from .stream import Stream


def main():
    with Stream() as s:
        messages: Iterator[NMEAMessage] = iter(s)
        while True:
            try:
                nmea = next(messages)
                if nmea.nmea_type == NMEAType.ENCAPSULATED:
                    ais = AISMessage(nmea)
                    print(ais)
                else:
                    print(f'Unsupported encoding for {nmea}')
            except StopIteration:
                messages = iter(s)
            except Exception:
                print_exc()


try:
    main()
except KeyboardInterrupt:
    pass
