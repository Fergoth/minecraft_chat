import asyncio
import json
import logging

logger = logging.getLogger(__name__)


async def register():
    reader, writer = await asyncio.open_connection("minechat.dvmn.org", 5050)

    response = await reader.readline()
    logger.debug(response.decode().strip())
    writer.write(b"\n")
    await writer.drain()

    response = await reader.readline()
    logger.debug(response.decode())
    nickname = input("Введите имя пользователя: ")
    writer.write(nickname.encode().strip().replace("/n", " ") + b"\n")
    await writer.drain()

    response = await reader.readline()
    logger.debug(json.loads(response))

    writer.close()
    await writer.wait_closed()
    return json.loads(response)["account_hash"]


async def main():
    account_hash = await register()
    logger.debug(account_hash)


if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    asyncio.run(main())
