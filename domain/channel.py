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
        self.queue = asyncio.Queue()
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self._process_queue(loop))

    def send(self, message: Message):
        self.queue.put_nowait(message.body.encode())

    async def _process_queue(self, loop):
        while True:
            data = await self.queue.get()
            sender_completed = loop.create_future()
            sender_connected = loop.create_connection(
                lambda: SenderProtocol(data, sender_completed),
                self.host,
                self.port
            )

            await sender_connected
            await sender_completed


class ReceiverChannel(Channel):
    """Receiver channel class"""
    def __init__(self, host=None, port=None):
        super().__init__(host, port)

        self.queue = asyncio.Queue()

        loop = asyncio.get_event_loop()

        coro = loop.create_server(
            lambda: ReceiverProtocol(self.queue),
            self.host,
            self.port
        )
        try:
            self.server = loop.run_until_complete(coro)
        except:
            raise OSError('Receiver channel unable to start')

    def close(self):
        loop = asyncio.get_event_loop()
        self.server.close()
        loop.run_until_complete(self.server.wait_closed())
