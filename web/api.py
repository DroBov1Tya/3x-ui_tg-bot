from config import http, fastapi_key

headers = {
    "X-API-Key": fastapi_key
}

async def send_data(hostname, passwd):
    j = {
        "hostname" : str(hostname),
        "port" : str("22"),
        "username" : str("root"),
        "passwd" : str(passwd)
    }

    r = await http(method="POST", url = "http://api:8000/add_server", headers=headers, json = j)
    return r

# 191.96.235.118:=3vn731U^n2D7546EnZg2y