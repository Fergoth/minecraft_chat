# MINECHAT 
Консольные утилиты для отправки и чтения сообщений в чат

## Утилиты
Утилита send_message.py отправляет сообщение в чат
Утилита read_message.py читает сообщения из чата и пишет их в лог

## Окружение
**В .env файле репозитория есть примеры переменных окружения!**
Так же можно передавать переменные как параметры скрипта и они перезапишут переменные окружения

## Установка
Для запуска требуется python версии 3.13. Или установленная утилита [uv](https://docs.astral.sh/uv/) 

## Установка зависимостей (если нет uv) 
```sh
pip install -r requirements.txt
```
### параметры запуска скрипта read_message.py
Или .env файл c начинающихся с READ (смотри пример в .env файле)

```
--host default="minechat.dvmn.org" Хост подключения к чату

--port", default=5000 Порт подключения к чату

--logfile", default="chat_log.txt" Файл для записи лога
```
### Пример запуска скрипта read_message.py
```sh
python read_message.py --host minechat.dvmn.org --port 5000 --logfile yourlog.txt
```
### При наличии uv
- Просто запустите скрипт с помощью uv 
```sh
uv run main.py --host minechat.dvmn.org --port 5000 --logfile yourlog.txt
```


### параметры запуска скрипта send_message.py
Или .env файл c начинающихся с SEND (смотри пример в .env файле)


--message", default="ТЕСТОВОЕ_СООБЩЕНИЕ" Сообщение для отправки  **Обязательный аргумент**
--host default="minechat.dvmn.org" Хост подключения к чату

--port", default=5050 Порт подключения к чату

--hash_filename", default="local_account.txt" Файл для хранения хеша пользователя

--nickname", default=None Имя пользователя для регистрации **Используется только если нет пользовательского хэша**

--token", default=None Токен пользователя. Если не указан ищем в --hash_filename

### Пример запуска скрипта send_message.py
```sh
python send_message.py --host minechat.dvmn.org --port 5000 --hash_filename yourhash.txt --message hello_world
```
Если локально хэша нет, будет предложено пройти регистрацию, если не будет указан никнейм, то будет предложено указать имя пользователя через консоль