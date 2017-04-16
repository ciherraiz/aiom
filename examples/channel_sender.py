from domain.channel import SenderChannel
from domain.message import Message
import asyncio
import datetime


async def five_messages(ch, loop):
    end_time = loop.time() + 60
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1) >= end_time:
            break
        item = Message(str(int(loop.time())))
        ch.send(item)
        await asyncio.sleep(5)

loop = asyncio.get_event_loop()

h = '127.0.0.1'
p = 8888
m = Message('Filipino')
sch = SenderChannel(h, p)

asyncio.ensure_future(five_messages(sch, loop))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.close()
