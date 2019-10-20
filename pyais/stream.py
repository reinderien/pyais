from socket import AF_INET, SOCK_STREAM, socket
from typing import Iterable
from .nmea_message import NMEAMessage, NMEAType


class Stream:
    """
    NMEA0183 stream via socket. Refer to
    https://en.wikipedia.org/wiki/NMEA_0183
    """

    BUF_SIZE = 4096

    def __init__(self, host: str = 'ais.exploratorium.edu', port: int = 80):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((host, port))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()

    def __iter__(self) -> Iterable[NMEAMessage]:
        return self._msg_loop()

    def _msg_loop(self) -> Iterable[NMEAMessage]:
        queue = []

        for line in self._recv_loop():
            try:
                msg = NMEAMessage(line)
            except Exception as e:
                raise ValueError(f'Failed to parse line "{line}"') from e

            if msg.nmea_type != NMEAType.ENCAPSULATED:
                yield(msg)  # Don't try to queue these
                continue

            if queue and not msg.follows(queue[-1]):
                print('Invalid queue transition from/to:\n'
                      f'   {queue[-1]}\n'
                      f'   {msg}')
                queue.clear()

            if msg.is_single():
                yield NMEAMessage.reduce([msg])
            elif msg.is_multi():
                queue.append(msg)
                if msg.sentence_index == msg.sentence_count:
                    yield NMEAMessage.reduce(queue)
                    queue.clear()
            else:
                raise ValueError(f'Invalid message queueable state for {msg}')

    def _recv_loop(self) -> Iterable[str]:
        partial = ''
        while True:
            body = self.sock.recv(self.BUF_SIZE).decode('ascii')

            # Can't use splitlines() because it does not produce empty lines where it should.
            # Need to call rstrip() because some lines are CRLF-terminated.
            lines = tuple(l.rstrip() for l in body.split('\n'))

            line = partial + lines[0]
            if line:
                yield line

            # yield from (line for line in lines[1:-1] if line)
            for line in lines[1:-1]:
                if line:
                    yield line
            partial = lines[-1]
