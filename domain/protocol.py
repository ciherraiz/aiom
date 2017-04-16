import asyncio
import logging
import sys
from domain.message import Message

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s: %(message)s',
    stream=sys.stderr,
)


class SenderProtocol(asyncio.Protocol):
    """Sender protocol class
    """
    def __init__(self, data: bytes, future: asyncio.Future):
        self.data = data
        self.log = logging.getLogger('SenderProtocol')
        self.future = future

    def connection_made(self, transport):
        """When the client succesfully connects to the server, it starts
        communicating immediately."""
        self.transport = transport
        self.transport.write(self.data)
        self.log.debug('sending {!r}'.format(self.data))
        if self.transport.can_write_eof():
            self.transport.write_eof()

    def eof_received(self):
        self.log.debug('received EOF')
        self.transport.close()
        if not self.future.done():
            self.future.set_result(True)

    def connection_lost(self, exc):
        self.log.debug('closing connection')
        self.transport.close()
        if not self.future.done():
            self.future.cancel()
            # self.future.set_result(False)


class ReceiverProtocol(asyncio.Protocol):
    """Receiver protocol class
    ReceiverProtocol handles client communication. Each new client connection
    creates a new protocol instance
    """
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue

    def connection_made(self, transport):
        """Each new client connection triggers a cal to connection_made
        The transport argument is an instance of asyncio.Transport, which
        provides an abstraction for doing asynchronous I/O using the socket"""
        self.transport = transport
        self.sender_address = transport.get_extra_info('peername')
        self.log = logging.getLogger(
            'ReceiverProtocol_{}_{}'.format(*self.sender_address)
        )
        self.log.debug('connection acepted')

    def data_received(self, data):
        """The protocol is invoked to pass the data in for processing
        Data is passed as a byte string, and it is up to the application to
        decode it in a appropiate way"""
        self.log.debug('received {!r}'.format(data))
        self.queue.put_nowait(data)

    def eof_received(self):
        """Some transports support a special end-of-file indicator (EOF)
        Because not all transports support an explicit EOF, this protocol
        asks the transport first."""
        self.log.debug('received EOF')
        if self.transport.can_write_eof():
            self.transport.write_eof()

    def connection_lost(self, error):
        """When a connection is closed, either normally or as the result of a
        error, the protocol's connection_lost method is callled. If there was
        an error, the argument contains an exception objet. Otherwise it is
        None"""
        if error:
            self.log.error('ERROR: {}'.format(error))
        else:
            self.log.debug('closing connection')
