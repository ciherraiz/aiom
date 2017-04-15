from domain.protocol import SenderProtocol, ReceiverProtocol
import asyncio


received_data = None


def message_handler(msg):
        global received_data
        received_data = msg


def test_send_data():
    global received_data
    sender_host = '127.0.0.1'
    receiver_host = '0.0.0.0'
    port = 8888
    msg = 'hello my friend!'
    data = msg.encode()

    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    """There are two steps to starting the server. First the application tells
    the event loop to create a new server object using the protocol class and
    the hostname and socket on which to listen. The create_server() method is a
    coroutine, so the results must be processed by the event loop in order to
    actually start the server. Completing the coroutine produces a asyncio.
    Server instance tied to the event loop
    """
    coror = loop.create_server(lambda: ReceiverProtocol(message_handler),
                               receiver_host,
                               port)

    receiver = loop.run_until_complete(coror)

    sender_completed = asyncio.Future()
    coros = loop.create_connection(
        lambda: SenderProtocol(data, sender_completed),
        sender_host,
        port
    )
    try:
        loop.run_until_complete(coros)
        loop.run_until_complete(sender_completed)
    except:
        print("test_send_a_message exception!")
    finally:
        receiver.close()
        loop.run_until_complete(receiver.wait_closed())
        # loop.close()

    assert data == received_data
