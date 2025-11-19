import asyncio
import json
import logging
from dataclasses import dataclass, asdict

from authorize import InvalidHash, authorize
from register import create_account

logger = logging.getLogger("chat_writer")


@dataclass
class Account:
    nickname: str
    account_hash: str


async def submit_message(reader, writer):
    new_message = input().strip().replace("\n", "")
    writer.write(new_message.encode() + b"\n")
    await writer.drain()
    message = await reader.readline()
    logger.info(message.decode())


async def main():
    try:
        account: Account = get_local_account()
    except FileNotFoundError:
        account: Account = Account(**await create_account())
        save_local_hash(account)
    except json.JSONDecodeError:
        logging.error("Невалидный json в local_account.txt, удалите файл и перепройдите регистрацию")
    logger.debug(f"Текущий хэш: {account.account_hash}")
    try:
        reader, writer = await authorize(account.account_hash)
        while True:
            await submit_message(reader, writer)
    except InvalidHash as e:
        logging.error(e)
        return
    finally:
        writer.close()
        await writer.wait_closed()


def get_local_account() -> Account:
    with open("local_account.txt", "r") as f:
        return Account(**json.load(f))


def save_local_hash(account: Account):
    with open("local_account.txt", "w") as f:
        json.dump(asdict(account), f)


if __name__ == "__main__":
    handler = logging.StreamHandler()
    formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formater)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    asyncio.run(main())
