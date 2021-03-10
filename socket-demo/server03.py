import socket
import subprocess  
import struct  # 制作报头的模块
import json   # 转换数据格式(序列化)

phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
phone.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 修复端口被占用的问题。
phone.bind(('127.0.0.1', 8848))
phone.listen(5)   # 监听，挂起连接数
while True:
    conn, client = phone.accept()  # 建立连接
    print("addr: ", client)
    while True:
        try:
            # 收命令
            cmd = conn.recv(8096)  # 长度足够收取命令
            print("cmd: ", cmd)

            # 执行命令、拿到结果
            obj = subprocess.Popen(cmd.decode('gbk'), shell=True,
                                   stdout=subprocess.PIPE,  # 存放正确的通道
                                   stderr=subprocess.PIPE)  # 存放错误的通道
            stdout = obj.stdout.read()  # 把里面的内容读出来放在这里
            stdeer = obj.stderr.read()

            # 把命令结果给客户端
            # 第一步：制作固定长度的报头
            header_dic = {
                'filename': 'a.txt',
                'total_size': len(stdeer) + len(stdout)  # 要发送数据的字节长度
            }      # 字典方便储存数据
            header_json = json.dumps(header_dic)  # 把字典转换成js格式(字符串类型)

            header_bytes = header_json.encode('gbk')  

            # 第二步：先发送报头的长度
            conn.send(struct.pack('i', len(header_bytes)))   
            
            # 第三步：再发报头
            conn.send(header_bytes)

            # 第四步：发送真实数据
            conn.send(stdout)
            conn.send(stdeer)
        except ConnectionResetError as err:
            print("err: ", err)
            break
    conn.close()

phone.close()