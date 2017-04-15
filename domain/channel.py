import asyncio
from domain.message import Message
from domain.protocol import SenderProtocol, ReceiverProtocol


class Channel:
    """Base channel class"""
    def __init__(self, host=None, port=None):
        self.host = host
        self.port = port


class SenderChannel(Channel):
    """Sender channel class"""
    def __init__(self, host=None, port=None):
        super().__init__(host, port)

    def send(self, message: Message):
        loop = asyncio.get_event_loop()
        sender_completed = asyncio.Future()
        coro = loop.create_connection(
            lambda: SenderProtocol(message.body.encode(), sender_completed),
            self.host,
            self.port
        )
        try:
            loop.run_until_complete(coro)
            loop.run_until_complete(sender_completed)
        except:
            raise OSError('Sender channel unable to send a message')


class ReceiverChannel(Channel):
    """Receiver channel class"""
    def __init__(self, host=None, port=None):
        super().__init__(host, port)
        loop = asyncio.get_event_loop()
        coro = loop.create_server(
            lambda: ReceiverProtocol(self._receive),
            self.host,
            self.port
        )
        try:
            self.server = loop.run_until_complete(coro)
        except:
            raise OSError('Receiver channel unable to start')

    def _receive(self, data: bytes):
        print(data)

    def close(self):
        loop = asyncio.get_event_loop()
        self.server.close()
        loop.run_until_complete(self.server.wait_closed())
