import asyncio
from domain.channel import ReceiverChannel
from domain.message import Message

h = '0.0.0.0'
p = 8888
loop = asyncio.get_event_loop()
rch = ReceiverChannel(h, p)

try:
    loop.run_forever()
finally:
    rch.close()
    loop.close()
