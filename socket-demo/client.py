import socket
import time
import struct


def newClient(host='localhost', port=8000):
    ADDR = (host, port)
    client = socket.socket()
    client.connect(ADDR)
    while True:
        msg = input('>>:').strip()
        if not msg:
            continue
        if msg == 'quit':
            break

        body = msg.encode(encoding='utf-8')
        header = [1, body.__len__(), 10001]
        headPack = struct.pack("!3I", *header)
        data = headPack+body

        sendlen = 0
        while sendlen < len(data):
            successlen = client.send(data[sendlen:])    # 返回发送成功的字节长度
            sendlen += successlen

        time.sleep(1)

        revcdata = client.recv(1024)
        print("revc: ", revcdata.decode(encoding='utf-8'))

    client.close()
    print("close")


def client_udp(host='localhost', port=8000):
    ADDR = (host, port)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        for data in [b'Michael', b'Tracy', b'Sarah', b'Ray', b'Brance']:
            sock.sendto(data, ADDR)
            time.sleep(1)
            print(sock.recv(1024).decode('utf-8'))


if __name__ == '__main__':
    newClient()
    # client_udp()
