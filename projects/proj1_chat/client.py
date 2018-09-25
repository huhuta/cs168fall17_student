import sys
import socket
from threading import Thread
from utils import CLIENT_MESSAGE_PREFIX


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
            message = raw_input(CLIENT_MESSAGE_PREFIX)
            data = '{name}|{channel}|{body}'.format(
                name=self.name, channel=self.channel, body=message).ljust(200)
            if message.startswith('/join') or message.startswith('/create'):
                self.channel = message.split(' ')[1]
            self.socket.sendall(data)

    def receive(self):
        while True:
            print(self.socket.recv(2048))

    def start(self):
        Thread(target=self.send).start()
        self.receive()


if __name__ == '__main__':
    name, address, port = sys.argv[1:]
    client = ChatClinet(name, address, port)
    client.start()
