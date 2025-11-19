import asyncio
import json
import logging

logger = logging.getLogger("chat_writer")


class InvalidHash(Exception):
    pass


async def authorize(account_hash: str) -> str:
    reader, writer = await asyncio.open_connection("minechat.dvmn.org", 5050)
    response = await reader.readline()
    writer.write(account_hash.encode() + b"\n")
    await writer.drain()

    response = await reader.readline()
    decoded_response = json.loads(response)
    logger.debug(decoded_response)
    if decoded_response is None:
        writer.close()
        await writer.wait_closed()
        raise InvalidHash("Неизвестный токен. Проверьте его или зарегистрируйте заново.")
    response = await reader.readline()
    logger.debug(response.decode())
    return reader, writer


async def main():
    hash = input("Введите account_hash: ")
    try:
        reader, writer = await authorize(hash)
    except InvalidHash as e:
        logging.error(e)
        return
    finally:
        writer.close()
        await writer.wait_closed()


if __name__ == "__main__":
    handler = logging.StreamHandler()
    formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formater)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    asyncio.run(main())
