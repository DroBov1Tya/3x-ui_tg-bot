import json
import random, uuid
import os
import logging
from src import generator_func
from config import http, endpoints
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)

#|=============================[Login]=============================|
async def login(username: str, password: str, webpath: str) -> dict:
    """
    Выполняет логин и возвращает заголовки с куки для последующих запросов.

    Args:
        username (str): Имя пользователя.
        password (str): Пароль пользователя.
        webpath (str): URL сервера для логина.

    Returns:
        dict: Заголовки с куки для последующих запросов или None в случае ошибки.
    """
    auth_data = {
        'username': username,
        'password': password
    }

    try:
        # Отправляем запрос на авторизацию
        response = await http(method="POST", url=f"{webpath}{endpoints['login']}", data=auth_data)

        # Логируем код ответа
        logger.info("Логин запрос завершён с кодом: %s", response.status_code)

        # Проверяем успешность запроса
        response.raise_for_status()

        # Извлекаем куки "3x-ui" из ответа
        session_cookie = response.cookies.get("3x-ui")
        if not session_cookie:
            logger.error("Куки '3x-ui' не найдены в ответе")
            return None

        # Создаем заголовки с куки для дальнейших запросов
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Cookie": f"3x-ui={session_cookie}"
        }

        logger.info("Логин успешен для пользователя: %s", username)
        return headers

    except Exception as ex:
        logger.error("Ошибка при логине для пользователя %s: %s", username, ex)
        return None
#--------------------------------------------------------------------------

#|=============================[Get List]=============================|
async def get_list(auth_headers):
    r = await http(url = endpoints["base_path"] + endpoints["list"], headers=auth_headers)
    remarks = r.json()["obj"]
    counter = 0
    for id in remarks:
        counter += 1
        print(f"[{counter}]{id['remark']}")
#--------------------------------------------------------------------------

#|=============================[Get Inbound]=============================|
async def get_inbound(auth_headers):
    r = await http(url = endpoints["base_path"] + endpoints["get_inbound"] + "1", headers=auth_headers)
    remarks = r.json()["obj"]
    print(remarks)
#--------------------------------------------------------------------------

#|=============================[Delete Inbound]=============================|
async def delete_inbound(auth_headers):
    r = await http(url = endpoints["base_path"] + endpoints["delete_inbound"] + "/1", headers=auth_headers)
    print(r)
#--------------------------------------------------------------------------

#|=============================[Add Client]=============================|
async def add_client(
        inbound_id: int,
        email: str,
        uuid: str,
        endpoints: dict,
        data: dict,
        enable: bool = True,
        flow: str = "",
        limit_ip: int = 0,
        total_gb: int = 0,
        expire_time: int = 0,
        telegram_id: str = "",
        subscription_id: str = "",
    ):

    settings = {
    "clients": [
        {
            "id": uuid,
            "email": email,
            "limitIp": limit_ip,
            "totalGB": total_gb,
            "expiryTime": expire_time,
            "enable": enable,
            "tgId": telegram_id,
            "subId": subscription_id
        }
    ],
    "decryption": "none",
    "fallbacks": []
}
        
    params = {
        "id": inbound_id,
        "settings": json.dumps(settings)
    }

    headers = await login(endpoints, data)
    r = await http(method="POST", url = endpoints["base_path"] + endpoints["add_client"], headers=headers, data=params)
    print(r)
    return 
#--------------------------------------------------------------------------

#|=============================[Add Inbound Request]=============================|
async def add_inbound_data(inbound_data: dict, webpath: str) -> None:
    """
    Отправляет данные для добавления inbound на сервер.

    Args:
        inbound_data (dict): Данные inbound для добавления.
        webpath (str): Веб-адрес сервера для отправки данных.

    Returns:
        None
    """
    try:
        settings = json.dumps({
        "clients": [
            {
                "id": inbound_data["client_id"],
                "email": inbound_data["email"],
                "limitIp": inbound_data["limit_ip"],
                "totalGB": inbound_data["total_gb"],
                "expiryTime": inbound_data["client_expiry_time"],
                "enable": inbound_data["enable"],
                "tgId": inbound_data["tg_id"],
                "subId": inbound_data["sub_id"],
                "reset": inbound_data["reset"]
            }
        ],
        "decryption": "none",
        "fallbacks": []
        })

        stream_settings = json.dumps({
        "network": inbound_data["network"],
        "security": inbound_data["security"],
        "realitySettings": {
            "dest": inbound_data["dest"],
            "serverNames": inbound_data["server_names"],
            "privateKey": inbound_data["private_key"],
            "shortIds" : inbound_data["short_ids"],
            "settings": {
                "fingerprint": inbound_data["fingerprint"],
                "publicKey": inbound_data["public_key"],
                "spiderX" : inbound_data["spiderx"]
            }
        },
        "tcpSettings": {
            "acceptProxyProtocol": False,
            "header": {
                "type": "none"
            }
        }
        })
    

        sniffing = json.dumps({
        "enabled": True,
        "destOverride": [
            "http",
            "tls",
            "quic",
            "fakedns"
        ],
        "metadataOnly": False,
        "routeOnly": False
        })
    
        # Объединение всех данных в один JSON
        data = json.dumps({
        "up": inbound_data["up"],
        "down": inbound_data["down"],
        "total": inbound_data["total"],
        "remark": inbound_data["remark"],
        "enable": inbound_data["enable"],
        "expiryTime": inbound_data["expiryTime"],
        "listen": inbound_data["listen"],
        "port": inbound_data["port"],
        "protocol": inbound_data["protocol"],
        # Три нижних параметра пришлось вынести отдельно для двойного энкодинга, тк конкретно в случае vless это является необходимостью
        "settings": settings,
        "streamSettings": stream_settings,
        "sniffing": sniffing
        })
    
        # Получение необходимых параметров
        endpoints = inbound_data["endpoints"]
        auth_headers = inbound_data["auth_headers"]

        response = await http(method="POST", url = webpath + endpoints["add_inbound"], data=data, headers=auth_headers)

        # Логирование статуса ответа
        logger.info("Запрос добавления inbound завершён с кодом: %s", response.status_code)

        # Проверка на ошибки
        response.raise_for_status()

    except json.JSONDecodeError as json_err:
        logger.error("Ошибка при сериализации данных в JSON: %s", json_err)
        raise
    except Exception as e:
        logger.error("Ошибка при отправке данных на сервер: %s", e)
        raise
#--------------------------------------------------------------------------

#|=============================[Add Inbound Init]=============================|
async def add_inbound(auth_headers: Dict[str, str], webpath: str, hostname: str, country: str, config_ttl: int) -> Tuple[Dict[str, Any], Any]:
    """
    Добавляет новый inbound сервер и возвращает данные о нем.

    Args:
        auth_headers (Dict[str, str]): Заголовки аутентификации.
        webpath (str): Путь к веб-ресурсу.
        hostname (str): Имя хоста для добавления.

    Returns:
        Tuple[Dict[str, Any], Any]: Словарь данных inbound сервера и результат создания конфигурации.
    """
    # Получаем ключи
    try:
        keygen_response = await http(method="POST", url=webpath + endpoints["keygen"], headers=auth_headers)
        keygen_response.raise_for_status()  # Проверяем на HTTP ошибки
        keys = keygen_response.json()['obj']
    except Exception as e:
        logger.error("Ошибка получения ключей: %s", e)
        raise
    
    # Генерация случайных данных
    remark = await generator_func.string_generator(type="letter", length=8)
    email = await generator_func.string_generator(type="letter", length=8)
    short_ids = await generator_func.random_short_ids()

    inbound_data = {
        "hostname": hostname,
        "endpoints": endpoints,
        "auth_headers": auth_headers,
        "up": 0,
        "down": 0,
        "total": 0,
        "remark": remark,
        "enable": True,
        "expiryTime": 0,
        "listen": "",
        "port": random.randint(1000, 65535),
        "protocol": "vless",
        "client_id": str(uuid.uuid4()),
        "email": email + "_" + country,
        "limit_ip": 0,
        "total_gb": 0,
        "client_expiry_time": config_ttl,
        "tg_id": "",
        "sub_id": await generator_func.string_generator(type="letdiggest", length=17),
        "reset": 0,
        "network": "tcp",
        "security": "reality",
        "dest": "yahoo.com:443",
        "server_names": ["yahoo.com", "www.yahoo.com"],
        "short_ids": short_ids,
        "private_key": keys["privateKey"],
        "public_key": keys["publicKey"],
        "fingerprint": "random",
        "spiderx": "/"
    }

    # Проверка на существование директории
    qr_code_dir = "qr_code"
    if not os.path.exists(qr_code_dir):
        os.makedirs(qr_code_dir)

    # Создание конфига и добавление данных
    try:
        config, qr_data = await generator_func.create_config(inbound_data)
        await add_inbound_data(inbound_data, webpath)
    except Exception as e:
        logger.error("Ошибка при создании конфигурации или добавлении данных: %s", e)
        raise

    return inbound_data, config, qr_data
#--------------------------------------------------------------------------
#|=============================[Add Inbound Init]=============================|
async def geo_ip(hostname):
    try:
        r = await http(url = "http://ip-api.com/json/" + hostname)
        r.raise_for_status()

        # Парсим ответ и проверяем наличие ключа 'country'
        response_json = r.json()
        country = response_json.get("countryCode")
    
        if country:
            return str(country)
        else:
            logger.error("Поле 'country' отсутствует в ответе для %s", hostname)
            return "Unknown"

    except Exception as e:
        logger.error("Ошибка при получении геолокации для %s: %s", hostname, e)
        return "Unknown"
#--------------------------------------------------------------------------