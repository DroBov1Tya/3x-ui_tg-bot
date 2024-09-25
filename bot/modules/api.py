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
            "tgid": message.from_user.id,
            "nickname": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name
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
async def admin_set(tgid):
    r = await http(f"http://api:8000/admin/set/{tgid}", method='GET', headers=headers)
    return r
#--------------------------------------------------------------------------
async def admin_unset(tgid):
    r = await http(f"http://api:8000/admin/unset/{tgid}", method='GET', headers=headers)
    return r
#--------------------------------------------------------------------------
async def admin_balance(tgid):
    r = await http(f"http://api:8000/admin/balance/", method='POST', data=d)
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
async def admin_level1(tgid):
    r = await http(f"http://api:8000/admin/level1/{tgid}", method='GET', headers=headers)
    return r
#--------------------------------------------------------------------------
async def admin_level2(tgid):
    r = await http(f"http://api:8000/admin/level2/{tgid}", method='GET', headers=headers)
    return r
#--------------------------------------------------------------------------
async def admin_level3(tgid):
    r = await http(f"http://api:8000/admin/level3/{tgid}", method='GET', headers=headers)
    return r
#--------------------------------------------------------------------------
async def admin_grep_users():
    r = await http(f"http://api:8000/admin/grepusers", method='GET', headers=headers)
    return r
#--------------------------------------------------------------------------
async def admin_fetchadmins():
    r = await http(f"http://api:8000/admin/fetchadmins", method='GET', headers=headers)
    return r
#--------------------------------------------------------------------------
async def test_country(tgid, hostname):

    encoded_hostname = urllib.parse.quote(hostname)
    server_info = await http(method='GET', url = f"http://api:8000/xui/server_info/{encoded_hostname}", headers = headers)
    d = {
        "hostname" : server_info["result"]["hostname"],
        "web_user" : server_info["result"]["web_user"],
        "web_pass" : server_info["result"]["web_pass"],
        "web_path" : server_info["result"]["web_path"],
        "tgid"     : tgid
    }

    r = await http(method='POST', url = "http://api:8000/xui/inbound_creation", headers=headers, data = d)
    print(r["qr_data"])

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