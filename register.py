import asyncio
import json
import logging

from utilities import open_async_connection

logger = logging.getLogger("chat_writer")


async def create_account(host: str, port: int, nickname: str | None = None) -> str:
    async with open_async_connection(host, port) as (reader, writer):
        reader, writer = await asyncio.open_connection(host, port)
        # Запрос на имя пользователя
        response = await reader.readline()
        logger.debug(response.decode())
        # Оставляем пустым чтобы ввести имя пользователя вместо хэша
        writer.write(b"\n")
        await writer.drain()

        response = await reader.readline()
        logger.debug(response.decode())
        if nickname is not None:
            writer.write(nickname.strip().replace("\n", " ").encode() + b"\n")
        else:
            input_nickname = input("Введите имя пользователя: ")
            writer.write(input_nickname.strip().replace("\n", " ").encode() + b"\n")
        await writer.drain()
        response = await reader.readline()
        logger.debug(json.loads(response))
    return json.loads(response)["account_hash"]


async def main() -> None:
    nickname = input("Enter your nickname: ")
    host = input("Enter host: ")
    port = int(input("Enter port: "))
    await create_account(host, port, nickname)


if __name__ == "__main__":
    handler = logging.StreamHandler()
    formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formater)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    asyncio.run(main())
