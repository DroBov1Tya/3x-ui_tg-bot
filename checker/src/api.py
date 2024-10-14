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

async def get_invoices():
    r = await http(method="GET", url="http://api:8000/cryptobot/get_invoices", headers=headers)
    return r.json()

async def process_invoices(json):
    paid = json.get("paid")
    expired = json.get("expired")

    for item in expired:
        await http(method="GET", url=f"http://api:8000/cryptobot/expired_invoices/{item}", headers=headers)
        
    for item in paid:
        await http(method="GET", url=f"http://api:8000/cryptobot/paid_invoices/{item}", headers=headers)
        r = await http(method="GET", url=f"http://api:8000/cryptobot/update_subscription/{item}", headers=headers)
        return r