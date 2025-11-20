import asyncio
import datetime
import logging

import aiofiles  # type: ignore
import configargparse  # type: ignore
from dotenv import load_dotenv

from utilities import open_async_connection

load_dotenv()

logger = logging.getLogger("based")


async def main():
    async with open_async_connection(args.host, args.port) as (reader, writer):
        while True:
            data = await reader.readuntil(separator=b"\n")
            current_time = datetime.datetime.now()
            logger.debug(
                f"[{current_time.strftime('%d.%m.%y %H:%M')}] {data.decode()}", end=""
            )
            async with aiofiles.open(f"{args.logfile}", mode="a") as f:
                await f.write(
                    f"[{current_time.strftime('%d.%m.%y %H:%M')}] {data.decode()}"
                )


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    parser = configargparse.ArgParser(
        auto_env_var_prefix="READ_",
    )
    parser.add("--host", default="minechat.dvmn.org", help="Hostname")
    parser.add("--port", default=5000, help="Port")
    parser.add("--logfile", default="chat_log.txt", help="Log file")
    args = parser.parse_args()
    asyncio.run(main())
