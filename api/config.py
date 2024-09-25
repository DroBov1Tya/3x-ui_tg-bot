import json
import httpx
import asyncpg
import os
import logging
from enum import Enum
from redis import asyncio as aioredis
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from fastapi_offline import FastAPIOffline
from fastapi import FastAPI
from typing import Any, Dict, List, Tuple, Optional

debug: bool = os.getenv('FASTAPI_DEBUG')
apikey: str = os.getenv('FASTAPI_KEY')
pg_conn: str = os.getenv('POSTGRES_DSN')
red_conn: str = os.getenv('REDIS_DSN')
red_ttl: int = os.getenv('REDIS_EXPIRE')

# VARS #
debug: bool = debug               # TURN OFF DEBUG ON PROD !!!
SECRET_VALUE: str = apikey       # CHANGE ME ON PROD !!!
SECRET_HEADER: str = 'X-API-Key'


docs_title: str = 'Xui API'
docs_description: str = 'Не лезь, убьёт!'

class Tags(Enum):
    user = "User"
    admin = "Admin"
    x_ui = "X-ui"


def auth401():
    X_API_KEY = APIKeyHeader(name=SECRET_HEADER)

    def api_key_auth(x_api_key: str = Depends(X_API_KEY)):
        if x_api_key != SECRET_VALUE:
            raise HTTPException(status_code=401, detail="Invalid API Key")

    auth_dep = [Depends(api_key_auth)]
    return auth_dep

def api_init():
    """
    Инициализирует и возвращает экземпляр FastAPI с учетом режима отладки.

    Args:
        debug (bool): Флаг, указывающий, находится ли приложение в режиме отладки.
        docs_title (str): Заголовок документации API.
        docs_description (str): Описание документации API.

    Returns:
        FastAPI: Экземпляр FastAPI с соответствующими настройками.
    """
    if debug is True:
        app = FastAPIOffline(
            title=docs_title,
            description=docs_description
        )
        logging.info("FastAPI app initialized in debug mode.")
    else:
        app = FastAPIOffline(
        # docs_url = None, # Disable docs (Swagger UI)
        # redoc_url = None, # Disable redoc
        dependencies = auth401(),
        title = docs_title,
        description = docs_description,
        )

    return app

    return app

# asyncpg wrapper

class PostgreSQL():
    def __init__(self):
        self.pool = None

    async def connect(self):
        if self.pool is None:
            self.pool = await asyncpg.create_pool(pg_conn)
            return self

    async def disconnect(self):
        if self.pool is not None:
            await self.pool.close()
            self.pool = None

    async def execute(self, query: str, args = ()):
        await self.connect()

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, *args)

    async def fetch(self, query: str, *args: Any, count: int = 1, cache: bool = False):
        await self.connect()

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                async for record in connection.cursor(query, *args):
                    if count == 1:
                        return dict(record)
                return None

    async def fetchall(self, query: str, args = ()):
        await self.connect()
        
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                return await connection.fetch(query, *args)

# aioredis wrapper
"""
Usage example:

redis_client = RedisClient()
await redis_client.set("mykey", "myvalue", expire=10)
value = await redis_client.get("mykey")
await redis_client.delete("mykey")
"""
class RedisClient:
    def __init__(self):
        self.redis = None
        self.dsn = red_conn  # Assuming you have the DSN in an environment variable

    async def connect(self):
        if self.redis is None:
            self.redis = await aioredis.from_url(self.dsn, db=1, decode_responses=True)
        return self.redis

    async def disconnect(self):
        if self.redis is not None:
            await self.redis.close()
            self.redis = None

    async def execute(self, command: str, *args):
        redis = await self.connect()
        return await redis.execute_command(command, *args)

    async def get(self, key: str):
        redis = await self.connect()
        return await redis.get(key)

    async def set(self, key: str, value, expire=red_ttl):
        redis = await self.connect()
        return await redis.set(key, value, ex=expire)

    async def delete(self, *keys):
        redis = await self.connect()
        return await redis.delete(*keys)

    # NEW!
    async def rpush(self, key: str, value: dict, expire: int = red_ttl * 2):
        redis = await self.connect()
        # Преобразование словаря в строку JSON перед добавлением в список
        value_str = json.dumps(value)
        # Добавление значения в список
        result = await redis.rpush(key, value_str)
        # Установка времени жизни для ключа
        if expire:
            await redis.expire(key, expire)
        return result

    # Method to retrieve and convert the list elements back to dictionaries
    async def lrange(self, key: str, start: int = 0, end: int = -1):
        redis = await self.connect()
        # Получаем элементы списка
        items = await redis.lrange(key, start, end)
        # Преобразуем JSON строки обратно в словари и возвращаем список словарей
        raw_items = [json.loads(item) for item in items]
        return [json.loads(item) for item in raw_items]

async def http(url: str, method: str = "GET", headers = None, data = None, json = None, file = None, proxies = None, verify = None, timeout = 120):
    timeout_config = httpx.Timeout(timeout)

    try:
        async with httpx.AsyncClient(proxies=proxies, headers=headers, verify=verify, follow_redirects=True, timeout=timeout_config) as req:
            if method != "POST":
                resp = await req.get(url=url) # [GET]
            elif file is None:
                resp = await req.post(url=url, data=data, json=json) # [POST] with json in body
            else:
                files = {'file': (file.filename, file.file)}
                resp = await req.post(url=url, files=files)# [POST] with file in body 

            result = resp

    except Exception as e:
        result = {"Success": False, "Reason": str(e)}

    return result


endpoints = {
    "login" :                       "/login",
    "list" :                        "/panel/api/inbounds/list",
    "get_inbound" :                 "/panel/api/inbounds/get/",
    "get_client" :                  "/panel/api/inbounds/getClientTraffics/{email}",
    "get_client_ip" :               "/panel/api/inbounds/clientIps/{email}",
    "add_inbound" :                 "/panel/api/inbounds/add",
    "add_client" :                  "/panel/api/inbounds/addClient",
    "update_inbound" :              "/panel/api/inbounds/update/{inboundId}",
    "update_client" :               "/panel/api/inbounds/updateClient/{uuid}",
    "reset_client_ip" :             "/panel/api/inbounds/clearClientIps/{email}",
    "reset_inbounds_stat" :         "/panel/api/inbounds/resetAllTraffics",
    "reset_inbound_clients_stat" :  "/panel/api/inbounds/resetAllClientTraffics/{inboundId}",
    "delete_inbound" :              "/panel/api/inbounds/del/",
    "delete_client" :               "/panel/api/inbounds/{inboundId}/delClient/{uuid}",
    "delete_depleted_dlients" :     "/panel/api/inbounds/delDepletedClients/{inboundId}",
    "online_clients" :              "/panel/api/inbounds/onlines",
    "export_database" :             "/panel/api/inbounds/createbackup",
    "keygen" :                      "/server/getNewX25519Cert"
    }