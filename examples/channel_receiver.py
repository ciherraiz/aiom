import asyncio
from domain.channel import ReceiverChannel

h = '0.0.0.0'
p = 8888
loop = asyncio.get_event_loop()
rch = ReceiverChannel(h, p)


try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    rch.close()
    loop.close()
