import socket
import struct

HOST = ''
PORT = 8000

dataBuffer = bytes()
headerSize = 12


def dataHandle(headPack, body):
    print("ver:%s, bodySize:%s, cmd:%s" % headPack)
    print(body.decode())
    print("")


if __name__ == '__main__':
    conn = None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            try:
                while True:
                    data = conn.recv(1024)
                    if data:
                        # 把数据存入缓冲区，类似于push数据
                        dataBuffer += data
                        while True:
                            if len(dataBuffer) < headerSize:
                                print("数据包（%s Byte）小于消息头部长度，跳出小循环" %
                                      len(dataBuffer))
                                break

                            # 读取包头
                            # struct中:!代表Network order，3I代表3个unsigned int数据
                            headPack = struct.unpack(
                                '!3I', dataBuffer[:headerSize])
                            bodySize = headPack[1]

                            # 分包情况处理，跳出函数继续接收数据
                            if len(dataBuffer) < headerSize+bodySize:
                                print("数据包（%s Byte）不完整（总共%s Byte），跳出小循环" %
                                      (len(dataBuffer), headerSize+bodySize))
                                break
                            # 读取消息正文的内容
                            body = dataBuffer[headerSize:headerSize+bodySize]

                            # 数据处理
                            dataHandle(headPack, body)

                            # 粘包情况的处理
                            # 获取下一个数据包，类似于把数据pop出
                            dataBuffer = dataBuffer[headerSize+bodySize:]
            except Exception as e:
                if conn:
                    conn.close()
                print("exit, e: {}".format(e))
