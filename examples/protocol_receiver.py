import asyncio
from domain.protocol import ReceiverProtocol
from domain.message import Message

loop = asyncio.get_event_loop()
loop.set_debug(True)

queue = asyncio.Queue()  # type: asyncio.Queue

received_message = None


def message_handler(msg):
        global received_message, receiver, loop
        received_message = msg


receiver_host = '0.0.0.0'
port = 8888
msg = 'hello my friend!'
message = Message(msg)

coror = loop.create_server(
    lambda: ReceiverProtocol(queue),
    receiver_host,
    port
)

try:
    receiver = loop.run_until_complete(coror)
    loop.run_forever()
except:
    print("Unable to start the receiver")
finally:
    receiver.close()
    loop.run_until_complete(receiver.wait_closed())
    loop.close()
