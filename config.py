import httpx


async def http(url: str, method: str = "GET", headers=None, data = None, files = None, cookie = None, text = None):
    try:
        async with httpx.AsyncClient() as req:
            if method != "POST":
                resp = await req.get(url=url, headers=headers) # [GET]
            elif files is None:
                resp = await req.post(url=url, json=data, headers=headers) # [POST] with json in body
            else:
                #files = {'file': (file.filename, file.file)}
                resp = await req.post(url=url, files=files, headers=headers)# [POST] with file in body 
            if cookie == True:
                result = resp.cookies
            elif text == True:
                result = resp.text
            else:
                result = resp.json()

    except Exception as e:
        result = {"Success": False, "Reason": str(e)}

    return result
