from domain.channel import Channel, SenderChannel, ReceiverChannel
from domain.message import Message


def test_create_a_channel():
    h = '127.0.0.1'
    p = 8888
    ch = Channel(host=h, port=p)
    assert ch.host == h and ch.port == p


"""
def test_send_a_message():
    h = '127.0.0.1'
    p = 8888
    m = Message("hey brother!")
    sch = SenderChannel(host=h, port=p)
    rch = ReceiverChannel(host=h, port=p)
    sch.send(m)
    assert m == rch.receive()
"""
