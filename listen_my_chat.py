import asyncio
import datetime
import logging

import aiofiles
import configargparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger("based")

async def main():
    reader, _ = await asyncio.open_connection(args.host, args.port)
    while True:
        data = await reader.readuntil(separator=b"\n")
        current_time = datetime.datetime.now()
        logger.debug(
            f"[{current_time.strftime('%d.%m.%y %H:%M')}] {data.decode()}", end=""
        )
        async with aiofiles.open("chat_log.txt", mode="a") as f:
            await f.write(
                f"[{current_time.strftime('%d.%m.%y %H:%M')}] {data.decode()}"
            )


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    parser = configargparse.ArgParser(
        auto_env_var_prefix="CHAT_",
    )
    parser.add("--host", default="minechat.dvmn.org", help="Hostname")
    parser.add("--port", default=5000, help="Port")
    parser.add("--logfile", default="chat_log.txt", help="Log file")
    args = parser.parse_args()
    asyncio.run(main())
