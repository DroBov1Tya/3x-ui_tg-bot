import redis.asyncio as aioredis

async def redis_get_all() -> dict:
    # Создаем подключение к Redis
    r = await aioredis.from_url('redis://redis:6379', decode_responses=True)
    
    # Получаем все ключи (хостнеймы)
    keys = await r.keys('*')  # Можно использовать шаблоны, если нужно

    # Если ключи не найдены, возвращаем пустой словарь
    if not keys:
        return {}

    # Получаем все значения по ключам
    values = await r.mget(keys)
    
    # Создаем словарь из ключей и значений
    result = dict(zip(keys, values))
    
    return result
