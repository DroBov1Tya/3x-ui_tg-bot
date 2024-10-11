from config import http, fastapi_key


headers = {
    "X-API-Key": fastapi_key
}

async def get_servers():
    r = await http(method="GET", url = "http://api:8000/servers/get_servers", headers=headers)
    return r.json()
#--------------------------------------------------------------------------

async def server_down(hostname):
    d = {
        "hostname" : hostname
    }

    r = await http(method="POST", url = "http://api:8000/servers/server_down", headers=headers, json=d)
    return r
#--------------------------------------------------------------------------

async def remove_configs(hostname):
    r = await http(method="GET", url = f"http://api:8000/xui/remove_configs/{hostname}", headers=headers)
    return r

async def restore_config_limits(hostname):
    r = await http(method="GET", url = f"http://api:8000/user/restore_config_limit/{hostname}", headers=headers)
    return r

