# import sys
from time import sleep
import select
import socket
from utils import *


class ChatServer(object):
    def __init__(self, port):
        self.server_socket = socket.socket()
        self.server_socket.bind(("", int(port)))
        self.server_socket.listen(5)
        self.server_socket.setblocking(False)
        self.socket_list = []
        self.socket_list.append(self.server_socket)
        self.message_buffer = {}

    def start(self):
        while True:
            sleep(1)
            ready_to_read, ready_to_write, in_error = select.select(
                self.socket_list, [], [], 0)
            for sock in ready_to_read:
                if sock == self.server_socket:
                    sockfd, addr = self.server_socket.accept()
                    self.socket_list.append(sockfd)
                    self.message_buffer[sockfd] = ''
                    print(addr)
                else:
                    msg = sock.recv(MESSAGE_LENGTH)
                    self.message_buffer[sock] += msg
                    if len(self.message_buffer[sock]) > 199:
                        data = self.message_buffer[sock][:200]
                        split_data = data.split('|')
                        name, channel = split_data[:2]
                        body = '|'.join(split_data[2:])
                        print(name)
                        print(channel)
                        print(body)
                        self.message_buffer[sock] = self.message_buffer[sock][200:]


if __name__ == '__main__':
    # port = sys.argv[1]
    port = 5000
    chat_server = ChatServer(port)
    chat_server.start()
