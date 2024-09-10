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