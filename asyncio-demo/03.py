import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    task1 = loop.create_task(
        say_after(1, 'hello'))

    task2 = asyncio.ensure_future(
        say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
