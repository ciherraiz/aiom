import asyncio
from domain.protocol import SenderProtocol
from domain.message import Message

sender_host = '127.0.0.1'
receiver_host = '0.0.0.0'
port = 8888
msg = 'hello my friend!'
message = Message(msg)

loop = asyncio.get_event_loop()
loop.set_debug(True)
sender_completed = asyncio.Future()
coros = loop.create_connection(
    lambda: SenderProtocol(message, sender_completed),
    sender_host,
    port
)
try:
    loop.run_until_complete(coros)
    loop.run_until_complete(sender_completed)
except:
    print("Unable to send the message!")
finally:
    loop.close()
