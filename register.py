import asyncio
import json
import logging

logger = logging.getLogger("chat_writer")


async def create_account(nickname: str = None) -> str:
    reader, writer = await asyncio.open_connection("minechat.dvmn.org", 5050)
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
        input_nickname = input("Enter your nickname: ")
        writer.write(input_nickname.strip().replace("\n", " ").encode() + b"\n")
    await writer.drain()

    response = await reader.readline()
    logger.debug(json.loads(response))

    writer.close()
    await writer.wait_closed()
    return json.loads(response)


async def main():
    nickname = input("Enter your nickname: ")
    await create_account(nickname)


if __name__ == "__main__":
    handler = logging.StreamHandler()
    formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formater)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    asyncio.run(main())
