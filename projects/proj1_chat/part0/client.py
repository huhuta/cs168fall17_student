import sys
import socket


def main(host, port):
    s = socket.socket()
    s.connect((host, int(port)))

    message = input('-> ')
    s.send(message.encode())
    s.close()


if __name__ == '__main__':
    host, port = sys.argv[1:]
    main(host, port)
    
