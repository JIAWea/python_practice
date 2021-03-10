# import socket
import asyncio


async def handle_client(reader, writer):
    request = None
    while request != 'quit':
        request = (await reader.read(255)).decode('utf-8')
        response = str(eval(request)) + '\n'
        writer.write(response.encode('utf-8'))
        await writer.drain()
    writer.close()

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server.bind(('localhost', 8000))
# server.listen(8)
# server.setblocking(False)


async def do_some_work(x):
    print('waiting '+str(x))
    await asyncio.sleep(x)
    print('done')

if __name__ == "__main__":
    # try:
    #     loop = asyncio.get_event_loop()
    #     loop.create_task(asyncio.start_server(
    #         handle_client, 'localhost', 8000))
    #     loop.run_forever()
    # finally:
    #     loop.close()

    loop = asyncio.get_event_loop()
    coros = [asyncio.ensure_future(do_some_work(x)) for x in range(1, 4)]
    # loop.run_until_complete(asyncio.gather(*coros))
    loop.run_forever()
    loop.close()
