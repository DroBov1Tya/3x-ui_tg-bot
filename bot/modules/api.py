import base64
import urllib.parse
import os
import tempfile
import logging
from asyncio import subprocess as sub
from asyncio import create_subprocess_exec as create_sub
from config import http, fastapi_url, fastapi_key

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
    r = await http(f"http://api:8000/user/create", method='POST', data=d, headers=headers)
    return r
#--------------------------------------------------------------------------
async def user_info(tgid): #DONE
    r = await http(f"http://api:8000/user/{tgid}", headers=headers)
    return r
#--------------------------------------------------------------------------
async def is_admin(tgid):
    r = await http(f"http://api:8000/admin/isadmin/{tgid}", headers=headers, method="GET")
    return r
#--------------------------------------------------------------------------
async def admin_ban(tgid):
    r = await http(f"http://api:8000/admin/ban/{tgid}", method='GET', headers=headers)
    return r
#--------------------------------------------------------------------------
async def admin_unban(tgid):
    r = await http(f"http://api:8000/admin/unban/{tgid}", method='GET', headers=headers)
    return r
#--------------------------------------------------------------------------
async def admin_create_voucher_one():
    r = await http(f"http://api:8000/admin/voucherone", method='GET', headers=headers)
    return r
#--------------------------------------------------------------------------
async def admin_create_voucher_six():
    r = await http(f"http://api:8000/admin/vouchersix", method='GET', headers=headers)
    return r
#--------------------------------------------------------------------------
async def admin_create_voucher_year():
    r = await http(f"http://api:8000/admin/voucheryear", method='GET', headers=headers)
    return r
#--------------------------------------------------------------------------
async def create_config(message, hostname):

    encoded_hostname = urllib.parse.quote(hostname)
    server_info = await http(method='GET', url = f"http://api:8000/xui/server_info/{encoded_hostname}", headers = headers)
    d = {
        "hostname" : server_info["result"]["hostname"],
        "web_user" : server_info["result"]["web_user"],
        "web_pass" : server_info["result"]["web_pass"],
        "web_path" : server_info["result"]["web_path"],
        "tgid"     : message.chat.id,
        "tg_nick"  : message.chat.username
    }

    r = await http(method='POST', url = "http://api:8000/xui/inbound_creation", headers=headers, data = d)
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
async def servers_count():
    r = await http(f"http://api:8000/xui/servers_count", method='GET', headers=headers)
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
        r = await http(f"http://api:8000/user/checkvoucher", method='POST', data=data)
        return r
    except Exception as ex:
        # Обработка ошибок
        return {"Success": False, "Reason": str(ex)}
#--------------------------------------------------------------------------
async def process_voucher(tgid: int, voucher: str):
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
        subscription_request = await http(f"http://api:8000/user/getsubscription/{tgid}", method='GET', headers=headers)

        data = {
                "tgid": tgid,
                "voucher_code": voucher,
                "subscription" : subscription_request.get("subscription")
            }

        r = await http(f"http://api:8000/user/activatevoucher", method='POST', data=data)
        return r
    except Exception as ex:
        # Обработка ошибок
        return {"Success": False, "Reason": str(ex)}
#--------------------------------------------------------------------------
async def getbalance(tgid: int):
    try:
        r = await http(f"http://api:8000/user/getbalance/{tgid}", method='GET', headers=headers)
        return r
    except Exception as ex:
        # Обработка ошибок
        return {"Success": False, "Reason": str(ex)}
#--------------------------------------------------------------------------
async def getsubsctiption(tgid: int):
    try:
        r = await http(f"http://api:8000/user/getsubscription/{tgid}", method='GET', headers=headers)
        return r
    except Exception as ex:
        # Обработка ошибок
        return {"Success": False, "Reason": str(ex)}
#--------------------------------------------------------------------------