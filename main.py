import asyncio
import datetime

import aiofiles


async def main():
    reader, _ = await asyncio.open_connection("minechat.dvmn.org", 5000)
    while True:
        data = await reader.readuntil(separator=b"\n")
        current_time = datetime.datetime.now()
        print(f"[{current_time.strftime('%d.%m.%y %H:%M')}] {data.decode()}", end="")
        async with aiofiles.open("chat_log.txt", mode="a") as f:
            await f.write(
                f"[{current_time.strftime('%d.%m.%y %H:%M')}] {data.decode()}"
            )


asyncio.run(main())
