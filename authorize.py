import asyncio
import json
import logging

from utilities import open_async_connection

logger = logging.getLogger("chat_writer")


class InvalidHash(Exception):
    pass


async def authorize(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter, account_hash: str
) -> None:
    response = await reader.readline()
    writer.write(account_hash.encode() + b"\n")
    await writer.drain()

    response = await reader.readline()
    decoded_response = json.loads(response)
    logger.debug(decoded_response)
    if decoded_response is None:
        writer.close()
        await writer.wait_closed()
        raise InvalidHash(
            "Неизвестный токен. Проверьте его или зарегистрируйте заново."
        )
    response = await reader.readline()
    logger.debug(response)


async def main():
    hash = input("Введите account_hash: ")
    host = input("Введите host: ")
    port = int(input("Введите port: "))
    async with open_async_connection(host, port) as (reader, writer):
        try:
            await authorize(hash)
        except InvalidHash as e:
            logging.error(e)
            return


if __name__ == "__main__":
    handler = logging.StreamHandler()
    formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formater)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    asyncio.run(main())
