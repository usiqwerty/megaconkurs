import asyncio, time
d=5
async def a():
    print('a1')
    time.sleep(1)
    await asyncio.sleep(d)
    print('a2')
    time.sleep(1)
    await asyncio.sleep(d)
    print('a3')
    time.sleep(1)
    await asyncio.sleep(d)
async def b():
    print('b1')
    time.sleep(1)
    await asyncio.sleep(d)
    print('b2')
    time.sleep(1)
    await asyncio.sleep(d)
    print('b3')
    time.sleep(1)
    await asyncio.sleep(d)
async def c():
    print('c1')
    time.sleep(1)
    await asyncio.sleep(d)
    print('c2')
    time.sleep(1)
    await asyncio.sleep(d)
    print('c3')
    time.sleep(1)
    await asyncio.sleep(d)

async def run():
    t1=asyncio.create_task(a())
    t2 = asyncio.create_task(b())
    t3 = asyncio.create_task(c())
    for x in t1, t2, t3:
        await x

asyncio.run(run())