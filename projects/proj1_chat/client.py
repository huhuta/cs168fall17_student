# import sys
import socket
from threading import Thread


class ChatClinet(object):
    def __init__(self, address, port):
        self.address = address
        self.port = int(port)
        self.socket = socket.socket()
        self.socket.connect((self.address, self.port))

    def send(self):
        while True:
            msg = raw_input('[Me] ')
            self.socket.send(msg)

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
    address = 'localhost'
    port = 5000
    client = ChatClinet(address, port)
    client.start()
