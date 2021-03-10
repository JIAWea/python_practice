import socket
from server01 import MsgContainer


mc = MsgContainer()


def start_client(addr, port):
    s = socket.socket()
    s.connect((addr, port))
    s.send(mc.pack_msg('解决分包问题'))
    s.send(mc.pack_msg('python'))
    s.close()


if __name__ == '__main__':
    start_client('127.0.0.1', 8801)
