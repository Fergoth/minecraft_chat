import asyncio


async def main():
    reader, _ = await asyncio.open_connection("minechat.dvmn.org", 5000)
    while True:
        data = await reader.readuntil(separator=b'\n')
        print(data.decode().strip())


asyncio.run(main())
