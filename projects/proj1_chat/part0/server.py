import sys
import socket


def main(port):
    serversocket = socket.socket()
    serversocket.bind(('localhost', int(port)))
    serversocket.listen(1)

    while True:
        (c, address) = serversocket.accept()
        message = c.recv(1024)
        tmp = message
        while tmp:
            tmp = c.recv(1024)
            print('tmp : ', tmp)
            message += tmp
        print(message.decode())
        c.close()


if __name__ == '__main__':
    port = sys.argv[1]
    main(port)
