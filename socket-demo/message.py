import struct

HEADER_LEN = 12


class MsgContainer():
    def __init__(self):
        self.header = "!3I"
        self.data = b''
        self.recv_data = b''
        self._recv_buff_data = b''

    # unpack data
    def parse(self, data: bytes):
        """
        unpack
        """
        self._recv_buff_data += data
        if len(data) < HEADER_LEN:
            return ''
        head_pack = struct.unpack(self.header,
                                  self._recv_buff_data[:HEADER_LEN])
        data_len = head_pack[1]

        if len(self._recv_buff_data) < data_len+HEADER_LEN:
            self._recv_buff_data += data
            return ''

        data = self._recv_buff_data[HEADER_LEN:HEADER_LEN+data_len]

        self._recv_buff_data = self._recv_buff_data[HEADER_LEN+data_len:]

        print("self._recv_buff_data: ", self._recv_buff_data,
              "len: ", len(self._recv_buff_data))
        return data.decode('utf-8')

    # pack data
    def serialize(self, client_id, stream_id, raw_data):
        header = [client_id, stream_id, raw_data.__len__()]
        headPack = struct.pack(self.header, *header)
        print("头部字节: ", headPack.__len__())
        return headPack+raw_data.encode(encoding='utf-8')


HEADER_LEN = 12
HEADER = "!3I"


class MsgHandler(object):
    def __init__(self):
        self.msg = []
        self.msg_buff = b''
        self.msg_len = 0

    def __add_zero(self, client_id, stream_id, raw_data_len):
        # 添加头部
        header = [client_id, stream_id, raw_data_len]
        headPack = struct.pack(self.header, *header)
        return headPack

    def pack_msg(self, data):
        """封装数据
        """
        bdata = data.encode(encoding='utf-8')
        return self.__add_zero(1, 1000, len(bdata)) + bdata

    def __get_msg_len(self):
        head_pack = struct.unpack(HEADER,
                                  self.msg_buff[:HEADER_LEN])
        self.msg_len = head_pack[1]

    def add_data(self, data):
        if len(data) == 0 or data is None:
            return
        self.msg_buff += data
        self.__check_head()

    def __check_head(self):
        if len(self.msg_buff) > HEADER_LEN:
            self.__get_msg_len()
            self.__get_msg()

    def __get_msg(self):
        if len(self.msg_buff)-HEADER_LEN >= self.msg_len:
            msg = self.msg_buff[HEADER_LEN:HEADER_LEN+self.msg_len]
            self.msg_buff = self.msg_buff[HEADER_LEN+self.msg_len:]
            self.msg_len = 0
            msg = msg.decode(encoding='utf-8')
            self.msg.append(msg)
            self.__check_head()

    def get_all_msg(self):
        return self.msg

    def clear_msg(self):
        self.msg = []
