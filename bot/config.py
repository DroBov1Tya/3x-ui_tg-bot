import httpx
import os

admins: list = os.getenv("ADMINS")
#|===========================[TG bot init]===========================|
if os.getenv("BOT_DEBUG"):
    bot_token: str = os.getenv("BOT_TOKEN_DEV")
else:
    bot_token: str = os.getenv("BOT_TOKEN_PROD")
#|===========================[End TG bot init]===========================|
#|=============================[Api keys]=============================|
fastapi_key: str = os.getenv("FASTAPI_KEY")
fastapi_url: str = "http://api:8000/"
#|===========================[End Api keys]===========================|

async def http(url: str, method: str = "GET", headers=None, data = None, files = None):
    try:
        async with httpx.AsyncClient() as req:
            if method != "POST":
                resp = await req.get(url=url, headers=headers) # [GET]
            elif files is None:
                resp = await req.post(url=url, json=data, headers=headers) # [POST] with json in body
            else:
                #files = {'file': (file.filename, file.file)}
                resp = await req.post(url=url, files=files, headers=headers)# [POST] with file in body 

            result = resp.json()

    except Exception as e:
        result = {"Success": False, "Reason": str(e)}

    return result
#|===========================[End Methods]=============================|

