import sys
import select
import socket
from utils import MESSAGE_LENGTH, SERVER_CLIENT_JOINED_CHANNEL, \
    SERVER_NO_CHANNEL_EXISTS, SERVER_CHANNEL_EXISTS, \
    SERVER_INVALID_CONTROL_MESSAGE


class ChatServer(object):
    def __init__(self, port):
        self.server_socket = socket.socket()
        self.server_socket.bind(('', int(port)))
        self.server_socket.listen(5)
        self.server_socket.setblocking(False)
        self.socket_list = []
        self.socket_list.append(self.server_socket)
        self.message_buffer = {}
        self.channels = {}

    def _control_message_process(self, name, body, sock):
        command_type, argument = body.split(' ')[:2]
        if command_type == '/create':
            if argument in self.channels:
                sock.sendall(SERVER_CHANNEL_EXISTS.format(argument))
                return
            self.channels[argument] = []
            self.channels[argument].append(sock)
        elif command_type == '/join':
            if argument not in self.channels:
                sock.sendall(SERVER_NO_CHANNEL_EXISTS.format(argument))
                return
            for channel_sock in self.channels[argument]:
                channel_sock.sendall(SERVER_CLIENT_JOINED_CHANNEL.format(name))
            self.channels[argument].append(sock)
        elif command_type == '/list':
            sock.sendall(' '.join(self.channels.keys()))
        else:
            sock.sendall(SERVER_INVALID_CONTROL_MESSAGE.format(command_type))

    def start(self):
        while True:
            ready_to_read, ready_to_write, in_error = select.select(
                self.socket_list, [], [])
            for sock in ready_to_read:
                if sock == self.server_socket:
                    sockfd, addr = self.server_socket.accept()
                    self.socket_list.append(sockfd)
                    self.message_buffer[sockfd] = ''
                else:
                    msg = sock.recv(MESSAGE_LENGTH)
                    self.message_buffer[sock] += msg
                    if len(self.message_buffer[sock]) > 199:
                        data = self.message_buffer[sock][:200].rstrip()
                        split_data = data.split('|')
                        name, channel = split_data[:2]
                        body = '|'.join(split_data[2:])

                        if body.startswith('/'):
                            self._control_message_process(name, body, sock)
                            self.message_buffer[sock] = self.message_buffer[sock][200:]
                        else:
                            for channel_socket in self.channels[channel]:
                                if channel_socket is not sock:
                                    channel_socket.sendall('[{0}] {1}'.format(name, body))


if __name__ == '__main__':
    port = sys.argv[1]
    chat_server = ChatServer(port)
    chat_server.start()
