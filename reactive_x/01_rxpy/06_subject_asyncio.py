import asyncio
import random
import threading
import time

from rx import operators as ops
from rx.scheduler.eventloop import AsyncIOScheduler, AsyncIOThreadSafeScheduler
from rx.subject import Subject, ReplaySubject

src = Subject()


# Emulate IO input stream
def random_push_source():
    count = 0
    while True:
        time.sleep(random.randint(1, 4))
        src.on_next(count)
        count += 1


threading.Thread(target=random_push_source).start()

loop = asyncio.get_event_loop()


async def main():
    rp = ReplaySubject()
    # src.subscribe(rp, scheduler=AsyncIOScheduler(loop=loop))
    src.pipe(
        ops.observe_on(scheduler=AsyncIOThreadSafeScheduler(loop=loop))
    ).subscribe(rp, scheduler=AsyncIOScheduler(loop=loop))

    print("Start wait")
    # await rp.pipe(ops.take(1))  # Block forever
    await rp.pipe(ops.take(1))

    print("Complete")


src.subscribe(lambda i: print(f"thread: {threading.currentThread().ident}. p = {i}"))
loop.run_until_complete(main())
