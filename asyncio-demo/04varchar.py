import asyncio

total = 0


async def increase():
    global total
    await asyncio.sleep(1)
    total += 1


async def decrease():
    global total
    await asyncio.sleep(0.1)
    total -= 1


async def increase_task():
    await asyncio.create_task(increase())


async def decrease_task():
    await asyncio.create_task(decrease())


async def add():
    global total
    for i in range(100):
        await asyncio.sleep(0.1)
        total += i


async def desc():
    global total
    for i in range(100):
        await asyncio.sleep(0.1)
        total -= i


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(
    #     asyncio.gather(*(increase_task() for _ in range(10000)), *(decrease_task() for _ in range(10000))),
    #     # asyncio.wait([increase_task() for _ in range(10000)]),
    # )

    loop.run_until_complete(
        asyncio.gather(*(add() for _ in range(1000)), *(desc() for _ in range(1000)))
    )
    print("total: ", total)

    loop.close()
