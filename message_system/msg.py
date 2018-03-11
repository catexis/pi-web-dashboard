import sys
import zmq


def send_message(msg):
    # Функция отправки сообщений на компьютер
    # Работает ТОЛЬКО на linux системах
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.LINGER, 0)
    socket.connect("tcp://192.168.1.4:5555")
    msg = str(msg).encode()
    socket.send(msg) # send can block on other socket types, so keep track
    # use poll for timeouts:
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    if poller.poll(3*1000): # 10s timeout in milliseconds
        msg = socket.recv()
    else:
        raise IOError("Timeout processing auth request")
    # these are not necessary, but still good practice:
    socket.close()
    context.term()
    sys.exit(0)


if __name__ == "__main__":
    send_message("hello")