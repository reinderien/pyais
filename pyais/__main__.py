from traceback import print_exc

from .ais_message import AISMessage
from .nmea_message import NMEAMessage
from .stream import Stream


def decode(nmea: NMEAMessage):
    if AISMessage.is_ais(nmea):
        try:
            ais = AISMessage(nmea)
            print(ais)
        except Exception as e:
            raise ValueError(f'Failed to decode AIS message "{nmea}"') from e
    else:
        print(f'Unsupported encoding for {nmea}')


def main():
    with Stream() as s:
        messages = iter(s)
        while True:
            try:
                decode(next(messages))
            except StopIteration:
                messages = iter(s)
            except Exception:
                print_exc()


try:
    main()
except KeyboardInterrupt:
    pass
