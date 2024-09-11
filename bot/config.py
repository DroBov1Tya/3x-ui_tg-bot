import httpx
import env

#|=============================[Api keys]=============================|
if env.TGBOT_DEBUG:
    bot_token = env.BOT_TOKEN_TEST
else:
    bot_token = env.BOT_TOKEN
#|===========================[End TG bot init]===========================|
fastapi_key = env.FASTAPI_KEY
fastapi_url = "http://api:8000/"
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

