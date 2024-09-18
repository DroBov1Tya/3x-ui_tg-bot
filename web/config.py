import httpx
from redis import asyncio as aioredis
import os

red_conn = os.getenv('REDIS_DSN')
red_ttl = os.getenv('REDIS_EXPIRE')


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