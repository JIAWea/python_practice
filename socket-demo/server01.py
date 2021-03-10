import socket

zero_count = 5


class MsgContainer(object):
    def __init__(self):
        self.msg = []
        self.msgpond = b''
        self.msg_len = 0

    def __add_zero(self, str_len):
        head = (zero_count - len(str_len))*'0' + str_len
        return head.encode(encoding='utf-8')

    def pack_msg(self, data):
        """
        封装数据
        :param data:
        :return:
        """
        bdata = data.encode(encoding='utf-8')
        str_len = str(len(bdata))
        return self.__add_zero(str_len) + bdata

    def __get_msg_len(self):
        self.msg_len = len(self.msgpond[:5])

    def add_data(self, data):
        if len(data) == 0 or data is None:
            return
        self.msgpond += data
        self.__check_head()

    def __check_head(self):
        if len(self.msgpond) > 5:
            self.__get_msg_len()
            self.__get_msg()

    def __get_msg(self):
        if len(self.msgpond)-5 >= self.msg_len:
            msg = self.msgpond[5:5+self.msg_len]
            self.msgpond = self.msgpond[5+self.msg_len:]
            self.msg_len = 0
            msg = msg.decode(encoding='utf-8')
            self.msg.append(msg)
            self.__check_head()

    def get_all_msg(self):
        return self.msg

    def clear_msg(self):
        self.msg = []


def start_server(port):
    HOST = '0.0.0.0'
    PORT = port

    # 定义socket类型，网络通信，TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))  # 套接字绑定的IP与端口
    s.listen(1)  # 开始TCP监听

    mc = MsgContainer()

    while True:
        conn, addr = s.accept()  # 接受TCP连接，并返回新的套接字与IP地址
        print('Connected by', addr)  # 输出客户端的IP地址

        while True:
            data = conn.recv(2048)       # 把接收的数据实例化
            print("data: ", data)
            # print(data)
            if len(data) == 0:
                break

            mc.add_data(data)          # 将数据写入缓冲区,每次写入都会尝试剥离实际传输的数据
            msgs = mc.get_all_msg()
            for msg in msgs:
                print(msg)

            mc.clear_msg()

        conn.close()  # 关闭连接


if __name__ == '__main__':
    start_server(8801)
