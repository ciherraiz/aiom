import asyncio
from domain.channel import Channel, SenderChannel, ReceiverChannel
from domain.message import Message



def test_create_a_channel():
    h = '127.0.0.1'
    p = 8888
    ch = Channel(host=h, port=p)
    assert ch.host == h and ch.port == p


def test_send_a_message():
    sh = '127.0.0.1'
    rh = '0.0.0.0'
    p = 8888
    m = Message('Filipino')
    sch = SenderChannel(sh, p)
    rch = ReceiverChannel(rh, p)
    try:
        sch.send(m)
        rm = rch.queue.get_nowait()
    finally:
        rch.close()
        # loop.close()
    assert m == rm
