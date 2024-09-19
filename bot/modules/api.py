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