import asyncio


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    n = 0
    while True:
        if n > 3:
            break
        n += 1
        await asyncio.sleep(1)
        print(f'Send: {message!r}')
        writer.write(message.encode())
        data = await reader.read(1024)
        if data == b'':
            break
        print(f'Received: {data.decode()!r}')

        # print('Close the connection')

    writer.close()

if __name__ == "__main__":
    asyncio.run(tcp_echo_client('Hello World!'))
