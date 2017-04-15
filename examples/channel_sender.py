from domain.channel import SenderChannel
from domain.message import Message

h = '127.0.0.1'
p = 8888
m = Message('Filipino')
sch = SenderChannel(h, p)
sch.send(m)
