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

    r = await http(method="POST", url = "http://api:8000/servers/add_server", headers=headers, json = j)
    return r

async def init_server(hostname):
    r = await http(method="POST", url="http://api:8000/xui/init_server", json={"hostname": hostname}, headers=headers)
    return r
# 191.96.235.118:=3vn731U^n2D7546EnZg2y