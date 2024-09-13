import httpx

async def http(url: str, method: str = "GET", headers = None, data = None, json = None, file = None, proxies = None, verify = None, timeout = 120):
    timeout_config = httpx.Timeout(timeout)

    try:
        async with httpx.AsyncClient(proxies=proxies, headers=headers, verify=verify, follow_redirects=True, timeout=timeout_config) as req:
            if method != "POST":
                resp = await req.get(url=url) # [GET]
            elif file is None:
                resp = await req.post(url=url, data=data, json=json) # [POST] with json in body
            else:
                files = {'file': (file.filename, file.file)}
                resp = await req.post(url=url, files=files)# [POST] with file in body 

            result = resp

    except Exception as e:
        result = {"Success": False, "Reason": str(e)}

    return result