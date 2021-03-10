# import logging
import asyncio
import selectors
import socket
# import struct
# import time
import types
from message import MsgHandler


# dataBuffer = bytes()
# headerSize = 12


# def dataHandle(headPack, body):
#     print('ver:%s, bodySize:%s, cmd:%s' % headPack)
#     print(body.decode())
#     print('')


# def start_server(host='0.0.0.0', port=8000):
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind((host, port))
#     s.listen(1)

#     try:
#         client, addr = s.accept()
#         print('connection by add [{}]'.format(addr))

#         while True:
#             data = client.recv(1024)
#             if data:
#                 # 把数据存入缓冲区，类似于push数据
#                 dataBuffer += data
#                 while True:
#                     if len(dataBuffer) < headerSize:
#                         print('数据包（%s Byte）小于消息头部长度，跳出小循环' %
#                             len(dataBuffer))
#                         break

#                     # 读取包头
#                     # struct中:!代表Network order，3I代表3个unsigned int数据
#                     headPack = struct.unpack(
#                         '!3I', dataBuffer[:headerSize])
#                     bodySize = headPack[1]

#                     # 分包情况处理，跳出函数继续接收数据
#                     if len(dataBuffer) < headerSize+bodySize:
#                         print('数据包（%s Byte）不完整（总共%s Byte），跳出小循环' %
#                             (len(dataBuffer), headerSize+bodySize))
#                         break
#                     # 读取消息正文的内容
#                     body = dataBuffer[headerSize:headerSize+bodySize]

#                     # 数据处理
#                     dataHandle(headPack, body)

#                     # 粘包情况的处理
#                     # 获取下一个数据包，类似于把数据pop出
#                     dataBuffer = dataBuffer[headerSize+bodySize:]
#     except Exception as e:
#         print('err: ', e)


# #### simple tcp socket #####
def start_tcp_server(host='0.0.0.0', port=8000):
    ADDR = (host, port)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(ADDR)
        sock.listen(1)
        while True:
            try:
                conn, address = sock.accept()
                print('addr of client: ', address)
                mc = MsgHandler()
                while True:
                    data = conn.recv(2)
                    if len(data) == 0:
                        break
                    print('data: ', data)
                    mc.add_data(data)
                    msgs = mc.get_all_msg()
                    for msg in msgs:
                        print("msg: ", msg)
                        conn.send(
                            ('response: '+msg).encode(encoding='utf-8'))
                    mc.clear_msg()
            except KeyboardInterrupt:
                print('exit')
            except Exception as e:
                conn.close()
                print('[Exception] e:', e)
# #### simple tcp socket #####


# #### simple udp socker ####
def start_udp_server(host='0.0.0.0', port=8000):
    ADDR = (host, port)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(ADDR)
        # sock.listen(1)
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                print('Received from %s:%s.' % addr)
                sock.sendto(b'Hello, %s!' % data, addr)

            except KeyboardInterrupt:
                print('exit')
            except Exception as e:
                break
                print('[Exception] e:', e)
# #### simple udp socker ####


# #### selectors #####
sel = selectors.DefaultSelector()


def multiconn_server(host='0.0.0.0', port=8000):

    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((host, port))
    lsock.listen()
    print('listening on', (host, port))
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)  # 有连接进来
            else:
                service_connection(key, mask)


def accept_wrapper(sock):
    conn, addr = sock.accept()
    print('accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('echoing', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
# #### selectors #####


# #### asyncio socker #####

clients = dict()


def client_connected_cb(client_reader, client_writer):
    # Use peername as client ID
    client_id = client_writer.get_extra_info('peername')

    print('Client connected: {}'.format(client_id))

    # Define the clean up function here
    def client_cleanup(fu):
        print('Cleaning up client {}'.format(client_id))
        # Retrievre the result and ignore whatever returned,
        # since it's just cleaning
        try:
            fu.result()
        except Exception:
            pass
        # Remove the client from client records
        del clients[client_id]

    task = asyncio.ensure_future(client_task(client_reader, client_writer))
    task.add_done_callback(client_cleanup)
    # Add the client and the task to client records
    clients[client_id] = task


async def client_task(reader, writer):
    client_addr = writer.get_extra_info('peername')
    print('Start echoing back to {}'.format(client_addr))

    while True:
        data = await reader.read(1024)
        if data == b'':
            print('Received EOF. Client disconnected.')
            return
        else:
            writer.write(data)
            await writer.drain()


def main():
    host = 'localhost'
    port = 8000
    loop = asyncio.get_event_loop()
    server_coro = asyncio.start_server(
        client_connected_cb, host=host, port=port, loop=loop)
    server = loop.run_until_complete(server_coro)

    try:
        print('Serving on {}:{}'.format(host, port))
        loop.run_forever()
    except KeyboardInterrupt:
        print('Keyboard interrupted. Exit.')

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

# #### asyncio socket #####


if __name__ == '__main__':
    start_tcp_server()
    # start_udp_server()
    # multiconn_server()
    # main()
