import socket
import struct
import json

phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
phone.connect(('127.0.0.1', 8848))
while True:
    # 发命令
    cmd = input('>>:').strip()
    if not cmd:
        continue
    phone.send(cmd.encode("gbk"))

    # 拿到命令结果
    # 第一步：先收取报头的长度
    obj = phone.recv(4)
    header_size = struct.unpack('i', obj)[0]

    # 第二步：再收报头
    header_bytes = phone.recv(header_size)

    # 第三步：从报头中间解析出对真是数据的描述信息
    header_json = header_bytes.decode('gbk')
    header_dic = json.loads(header_json)
    print(header_dic)
    total_size = header_dic['total_size']

    # 第三步：接受真实的数据
    recv_size = 0
    recv_data = b''
    while recv_size < total_size:
        res = phone.recv(1024)
        recv_data += res
        recv_size += len(res)
    print(recv_data.decode("gbk"))

phone.close()
