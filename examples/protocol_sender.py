import asyncio
from domain.protocol import SenderProtocol

sender_host = '127.0.0.1'
receiver_host = '0.0.0.0'
port = 8888
data = 'hello my friend!'.encode()

loop = asyncio.get_event_loop()
loop.set_debug(True)
sender_completed = asyncio.Future()
coro = loop.create_connection(
    lambda: SenderProtocol(data, sender_completed),
    sender_host,
    port
)
try:
    loop.run_until_complete(coro)
    loop.run_until_complete(sender_completed)
except:
    print("Unable to send the message!")
finally:
    loop.close()
