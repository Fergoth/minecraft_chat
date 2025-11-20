import asyncio
import json
import logging

import configargparse  # type: ignore
from dotenv import load_dotenv

from authorize import InvalidHash, authorize
from register import create_account
from utilities import open_async_connection


load_dotenv()
logger = logging.getLogger("chat_writer")


def save_local_hash(filename: str, hash: str):
    with open(filename, "w") as f:
        json.dump(hash, f)
    logger.info(f"Хеш сохранен в {filename}")


def load_hash_from_file(filename: str) -> str:
    with open(filename, "r") as f:
        return json.load(f)


async def submit_message(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter, message: str
):
    encoded_message = message.strip().replace("\n", "").encode() + b"\n\n"
    writer.write(encoded_message)
    await writer.drain()
    logger.info(f"Отправлено сообщение: {message}")


async def main():
    if args.token is not None:
        hash = args.token
    else:
        try:
            hash = load_hash_from_file(args.hash_filename)
        except FileNotFoundError:
            logger.info("Сохраненный хеш не найден, регистрируем пользователя")
            hash = await create_account(args.host, args.port, args.nickname)
        except json.JSONDecodeError:
            logging.error(
                "Невалидный json в local_account.txt, удалите файл и перепройдите регистрацию"
            )
            return
    save_local_hash(args.hash_filename, hash)
    logger.debug(f"Текущий хэш: {hash}")
    async with open_async_connection(args.host, args.port) as (reader, writer):
        try:
            await authorize(reader, writer, hash)
            await submit_message(reader, writer, args.message)
        except InvalidHash as e:
            logger.error(e)
            return


if __name__ == "__main__":
    handler = logging.StreamHandler()
    formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formater)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    parser = configargparse.ArgParser(
        auto_env_var_prefix="SEND_",
    )
    parser.add("--message", help="Сообщения для отправления", required=True)
    parser.add("--host", default="minechat.dvmn.org", help="Хост")
    parser.add("--port", default=5050, help="Порт")
    parser.add(
        "--token",
        default=None,
        help="Токен пользователя. Если не указан ищем в --hash_filename",
    )
    parser.add("--nickname", default=None, help="Имя пользователя для регистрации")
    parser.add(
        "--hash_filename", default="local_account.txt", help="Файл для хранения хеша"
    )
    args = parser.parse_args()
    logger.debug(f"{args}")

    asyncio.run(main())
