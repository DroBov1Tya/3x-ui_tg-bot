import base64
import urllib.parse
import os
import tempfile
from asyncio import subprocess as sub
from asyncio import create_subprocess_exec as create_sub
from config import http, fastapi_url, fastapi_key, logger
from config import onemonth, sixmonth, year

headers = {
    "X-API-Key": fastapi_key
}

#|=============================[Api requests]=============================|
async def create_user(message):
    d = {
        "user": {
            "tgid": message.chat.id,
            "nickname": message.chat.username,
            "first_name": message.chat.first_name,
            "last_name": message.chat.last_name
        }
    }
    r = await http(f"{fastapi_url}/user/create", method='POST', data=d, headers=headers)
    return r
#--------------------------------------------------------------------------

async def user_info(tgid): #DONE
    r = await http(f"{fastapi_url}/user/{tgid}", headers=headers)
    return r
#--------------------------------------------------------------------------

async def agree(tgid):
    r = await http(f"{fastapi_url}/user/agree/{tgid}", headers=headers)
    return r
#--------------------------------------------------------------------------

async def is_admin(tgid):
    r = await http(f"{fastapi_url}/admin/isadmin/{tgid}", headers=headers, method="GET")
    return r
#--------------------------------------------------------------------------

async def admin_ban(tgid):
    r = await http(f"{fastapi_url}/admin/ban/{tgid}", method='GET', headers=headers)
    return r
#--------------------------------------------------------------------------

async def admin_unban(tgid):
    r = await http(f"{fastapi_url}/admin/unban/{tgid}", method='GET', headers=headers)
    return r
#--------------------------------------------------------------------------

async def admin_create_voucher_one():
    r = await http(f"{fastapi_url}/admin/voucher_one", method='GET', headers=headers)
    return r
#--------------------------------------------------------------------------

async def admin_create_voucher_six():
    r = await http(f"{fastapi_url}/admin/voucher_one", method='GET', headers=headers)
    return r
#--------------------------------------------------------------------------

async def admin_create_voucher_year():
    r = await http(f"{fastapi_url}/admin/voucher_one", method='GET', headers=headers)
    return r
#--------------------------------------------------------------------------

async def create_config(message, hostname, config_ttl):

    encoded_hostname = urllib.parse.quote(hostname)
    server_info = await http(method='GET', url = f"{fastapi_url}/xui/server_info/{encoded_hostname}", headers = headers)
    d = {
        "hostname" : server_info["result"]["hostname"],
        "web_user" : server_info["result"]["web_user"],
        "web_pass" : server_info["result"]["web_pass"],
        "web_path" : server_info["result"]["web_path"],
        "tgid"     : message.chat.id,
        "tg_nick"  : message.chat.username,
        "config_ttl" : config_ttl
    }

    r = await http(method='POST', url = f"{fastapi_url}/xui/inbound_creation", headers=headers, data = d)
    if not r["Success"]:
        return False, None
    else:
        qr_code_dir = "qr_code"
        if not os.path.exists(qr_code_dir):
            os.makedirs(qr_code_dir)

        qr_byte = base64.b64decode(r["qr_data"])

        with tempfile.NamedTemporaryFile(delete=False, dir=qr_code_dir, suffix=".png") as temp_qr_file:
            temp_qr_file.write(qr_byte)  # Записываем данные QR-кода в файл
            temp_qr_file_path = temp_qr_file.name
        return r, temp_qr_file_path
#--------------------------------------------------------------------------

async def check_config_limit(tgid):
    r = await http(f"{fastapi_url}/user/config_limit/{tgid}", method='GET', headers=headers)
    return r
#--------------------------------------------------------------------------

async def reduce_config_limit(tgid):
    r = await http(f"{fastapi_url}/user/reduce_config_limit/{tgid}", method='GET', headers=headers)
    return r
#--------------------------------------------------------------------------

async def servers_count():
    r = await http(f"{fastapi_url}/xui/servers_count", method='GET', headers=headers)
    return r
#--------------------------------------------------------------------------

async def check_voucher(tgid: int, voucher: str):
    """
    Функция для отправки запроса в API для проверки ваучера.

    Args:
        tgid (int): Идентификатор пользователя Telegram (tgid).
        voucher (str): Код ваучера.

    Returns:
        dict: Ответ от API с результатом проверки ваучера.
    """
    # Формируем данные для отправки
    data = {
        "tgid": tgid,
        "voucher_code": voucher
    }

    # Отправляем POST-запрос в API для проверки ваучера
    try:
        r = await http(f"{fastapi_url}/user/check_voucher", method='POST', data=data, headers=headers)
        return r
    except Exception as ex:
        # Обработка ошибок
        return {"Success": False, "Reason": str(ex)}
#--------------------------------------------------------------------------

async def process_voucher(tgid: int, voucher: str, lang: str):
    """
    Функция для отправки запроса в API для активации ваучера.

    Args:
        tgid (int): Идентификатор пользователя Telegram (tgid).
        voucher (str): Код ваучера.

    Returns:
        dict: Ответ от API с результатом активации ваучера.
    """
    
    # Отправляем POST-запрос в API для активации ваучера
    try:
        subscription_request = await http(f"{fastapi_url}/user/get_subscription/{tgid}", method='GET', headers=headers)

        data = {
                "tgid": tgid,
                "voucher_code": voucher,
                "lang" : lang,
                "subscription" : subscription_request.get("subscription")
            }

        print(data)
        
        r = await http(f"{fastapi_url}/user/activate_voucher", method='POST', data=data, headers=headers)
        return r
    except Exception as ex:
        # Обработка ошибок
        return {"Success": False, "Reason": str(ex)}
#--------------------------------------------------------------------------

async def getsubsctiption(tgid: int):
    try:
        r = await http(f"{fastapi_url}/user/get_subscription/{tgid}", method='GET', headers=headers)
        return r
    except Exception as ex:
        # Обработка ошибок
        return {"Success": False, "Reason": str(ex)}
#--------------------------------------------------------------------------

async def set_language(tgid, lang):
    data = {
        "lang" : lang,
        "tgid" : tgid
    }
    try:
        r = await http(method="POST", url=f"{fastapi_url}/user/set_language", data=data, headers=headers)
        return r
    except Exception as ex:
        return {"Success": False, "Reason": str(ex)}
#--------------------------------------------------------------------------

async def check_language(tgid):
    try:
        r = await http(f"{fastapi_url}/user/check_language/{tgid}", method='GET', headers=headers)
        return r
    except Exception as ex:
        return {"Success": False, "Reason": str(ex)}
#--------------------------------------------------------------------------

async def get_crypto_prices_btc():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,litecoin,the-open-network&vs_currencies=usd"

    try:
        response = await http(url=url, method="GET")
        if response is None:
            logger.error(f"Error fetching BTC data: {response}")
            return {"Success": False, "Reason": "No response data"}
        else:
            return float(response['bitcoin']['usd'])
        
    except Exception as ex:
        logger.error(f"Exception occurred while fetching BTC data: {str(ex)}")
        return {"Success": False, "Reason": str(ex)}
#--------------------------------------------------------------------------

# Функция для получения цены Litecoin
async def get_crypto_prices_ltc():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,litecoin,the-open-network&vs_currencies=usd"

    try:
        response = await http(url=url, method="GET")
        if response is None:
            logger.error(f"Error fetching LTC data: {response}")
            return {"Success": False, "Reason": "No response data"}
        else:
            return float(response['litecoin']['usd'])
        
    except Exception as ex:
        logger.error(f"Exception occurred while fetching LTC data: {str(ex)}")
        return {"Success": False, "Reason": str(ex)}
#--------------------------------------------------------------------------

# Функция для получения цены TON
async def get_crypto_prices_ton():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,litecoin,the-open-network&vs_currencies=usd"

    try:
        response = await http(url=url, method="GET")
        if response is None:
            logger.error(f"Error fetching TON data: {response}")
            return {"Success": False, "Reason": "No response data"}
        else:
            return float(response['the-open-network']['usd'])
        
    except Exception as ex:
        logger.error(f"Exception occurred while fetching TON data: {str(ex)}")
        return {"Success": False, "Reason": str(ex)}
#--------------------------------------------------------------------------

async def calculate_subscription_prices(crypto_type):
    try:
        # Цена подписки в долларах
        one_month_usd: int = onemonth # Стоимость за 1 месяц
        six_month_usd: int = sixmonth  # Стоимость за 6 месяцев с учетом скидки
        twelve_month_usd: int = year 

        if crypto_type == "BTC":
            crypto_price: float = await get_crypto_prices_btc()

            six_month_crypto = six_month_usd / crypto_price
            twelve_month_crypto = (twelve_month_usd * 1.08) / crypto_price  # 18% скидка

            return round(six_month_crypto, 5), round(twelve_month_crypto, 7)

        elif crypto_type =="LTC":
            crypto_price: float = await get_crypto_prices_ltc()

            one_month_crypto = one_month_usd / crypto_price
            six_month_crypto = six_month_usd / crypto_price  # 9% скидка
            twelve_month_crypto = twelve_month_usd / crypto_price  # 18% скидка

            return round(one_month_crypto, 3), round(six_month_crypto, 3), round(twelve_month_crypto, 3)

        elif crypto_type == "TON":
            crypto_price: float = await get_crypto_prices_ton()

            one_month_crypto = one_month_usd / crypto_price
            six_month_crypto = six_month_usd / crypto_price  # 9% скидка
            twelve_month_crypto = twelve_month_usd / crypto_price  # 18% скидка

            return round(one_month_crypto, 2), round(six_month_crypto, 2), round(twelve_month_crypto, 2)
    
    except Exception as ex:
        logger.error(f"Exception occurred while fetching crypto data: {str(ex)}")
        return None, None, None
#--------------------------------------------------------------------------
