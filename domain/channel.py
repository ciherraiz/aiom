from domain.message import Message


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
        pass


class ReceiverChannel(Channel):
    """Receiver channel class"""
    def __init__(self, host=None, port=None):
        super().__init__(host, port)

    def receive(self) -> Message:
        pass
