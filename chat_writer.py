import asyncio
import logging
from register import create_account

logger = logging.getLogger('chat_writer')

async def main():
    if get_local_hash() is None:
        nickname = input("Enter your nickname: ")
        hash = await create_account(nickname)
        save_local_hash(hash)
    logger.debug(f"Local hash: {hash}")
    reader, writer = await asyncio.open_connection("minechat.dvmn.org", 5050)
    try:
        while True:
            new_message = input().strip().replace("\n", "")
            writer.write(new_message.encode() + b"\n")
            await writer.drain()
            await reader.readline()
            logger.info(await reader.readline().decode())
    finally:
        writer.close()
        await writer.wait_closed()


def get_local_hash():
    pass


def save_local_hash(hash):
    pass


if __name__ == "__main__":
    handler = logging.StreamHandler()
    formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formater)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    asyncio.run(main())
