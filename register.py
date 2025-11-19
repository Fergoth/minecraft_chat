import asyncio
import json
import logging

logger = logging.getLogger("chat_writer")


async def create_account(nickname: str) -> str:
    reader, writer = await asyncio.open_connection("minechat.dvmn.org", 5050)
    response = await reader.readline()
    logger.debug(response.decode().strip())
    writer.write(b"\n")
    await writer.drain()

    response = await reader.readline()
    logger.debug(response.decode())
    writer.write(nickname.strip().replace("\n", " ").encode() + b"\n")
    await writer.drain()

    response = await reader.readline()
    logger.debug(json.loads(response))

    writer.close()
    await writer.wait_closed()
    return json.loads(response)["account_hash"]


async def main():
    account_hash = await create_account()
    logger.debug(account_hash)


if __name__ == "__main__":
    handler = logging.StreamHandler()
    formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formater)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    asyncio.run(main())
