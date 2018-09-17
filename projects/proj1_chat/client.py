# import sys
import socket
from threading import Thread


class ChatClinet(object):
    def __init__(self, name, address, port):
        self.name = name
        self.address = address
        self.port = int(port)
        self.socket = socket.socket()
        self.socket.connect((self.address, self.port))
        self.channel = None

    def send(self):
        while True:
            message = raw_input('[Me] ')
            # # TODO handle no channel error
            # if not self.channel:
            data = '{name}|{channel}|{body}'.format(
                name=self.name, channel='test_channel', body=message).ljust(200)
            self.socket.sendall(data)

    def receive(self):
        while True:
            msg = self.socket.recv(1024)
            print(msg)

    def start(self):
        t = Thread(target=self.send)
        t.start()
        self.receive()


if __name__ == '__main__':
    # host, port = sys.argv[1:]
    name = 'test1'
    address = 'localhost'
    port = 5000
    client = ChatClinet(name, address, port)
    client.start()
