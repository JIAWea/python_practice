# -*- coding: utf-8 -*-
import asyncio
import threading
from datetime import datetime


async def add(a, b):
    await asyncio.sleep(1)
    return a + b


async def master_thread(loop):
    print("{} master: 1+2={}, thread: {}".format(datetime.now(), await add(1, 2), threading.currentThread().name))


def slave_thread(loop):
    # 注意：这不是 coroutine 函数
    import time
    time.sleep(2)

    f = asyncio.run_coroutine_threadsafe(add(1, 2), loop)
    print("{} slave: 1+2={}, thread: {}".format(datetime.now(), f.result(), threading.currentThread().name))


async def task():
    await asyncio.sleep(0.2)
    print("task...")


async def main(loop):
    await asyncio.gather(
        master_thread(loop),
        # 线程池内执行
        loop.run_in_executor(None, slave_thread, loop),
    )
    # fut = asyncio.run_coroutine_threadsafe(task(), loop)
    # fut = loop.call_soon_threadsafe(slave_thread, loop)

    loop.run_in_executor(None, slave_thread, loop),

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
