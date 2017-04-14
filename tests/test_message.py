from domain.message import Message


def test_the_body_message():
    m = 'The body message'
    msg = Message(data=m)
    assert msg.body == m
