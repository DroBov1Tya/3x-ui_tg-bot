import json
import random, uuid
import os
from src import generator_func
from config import http, endpoints

#|=============================[Login]=============================|
async def login(username, password, webpath): 
    auth_data = {
        'username': username,
        'password': password
    }

    r = await http(method="POST", url=webpath + endpoints["login"] , data=auth_data)
    session_cookie = r.cookies.get("3x-ui")

    if session_cookie:
        print(f"Login successful")

    headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Cookie": f"3x-ui={session_cookie}"  # Добавляем куку в заголовки запроса
        }
    if r is None:
        return None
    else:
        return headers
#--------------------------------------------------------------------------

#|=============================[Init]=============================|
async def init(username, password, webpath):
    auth_headers = await login(username, password, webpath)
#--------------------------------------------------------------------------

#|=============================[Get List]=============================|
async def get_list(auth_headers):
    r = await http(url = endpoints["base_path"] + endpoints["list"], headers=auth_headers)
    remarks = r.json()["obj"]
    counter = 0
    for id in remarks:
        counter += 1
        print(f"[{counter}]{id['remark']}")
#--------------------------------------------------------------------------

#|=============================[Get Inbound]=============================|
async def get_inbound(auth_headers):
    r = await http(url = endpoints["base_path"] + endpoints["get_inbound"] + "1", headers=auth_headers)
    remarks = r.json()["obj"]
    print(remarks)
#--------------------------------------------------------------------------

#|=============================[Delete Inbound]=============================|
async def delete_inbound(auth_headers):
    r = await http(url = endpoints["base_path"] + endpoints["delete_inbound"] + "/1", headers=auth_headers)
    print(r)
#--------------------------------------------------------------------------

#|=============================[Add Client]=============================|
async def add_client(
        inbound_id: int,
        email: str,
        uuid: str,
        endpoints: dict,
        data: dict,
        enable: bool = True,
        flow: str = "",
        limit_ip: int = 0,
        total_gb: int = 0,
        expire_time: int = 0,
        telegram_id: str = "",
        subscription_id: str = "",
    ):

    settings = {
    "clients": [
        {
            "id": uuid,
            "email": email,
            "limitIp": limit_ip,
            "totalGB": total_gb,
            "expiryTime": expire_time,
            "enable": enable,
            "tgId": telegram_id,
            "subId": subscription_id
        }
    ],
    "decryption": "none",
    "fallbacks": []
}
        
    params = {
        "id": inbound_id,
        "settings": json.dumps(settings)
    }

    headers = await login(endpoints, data)
    r = await http(method="POST", url = endpoints["base_path"] + endpoints["add_client"], headers=headers, data=params)
    print(r)
    return 
#--------------------------------------------------------------------------

#|=============================[Add Inbound Request]=============================|
async def add_inbound_data(inbound_data, webpath):
    settings = json.dumps({
    "clients": [
        {
            "id": inbound_data["client_id"],
            "email": inbound_data["email"],
            "limitIp": inbound_data["limit_ip"],
            "totalGB": inbound_data["total_gb"],
            "expiryTime": inbound_data["client_expiry_time"],
            "enable": inbound_data["enable"],
            "tgId": inbound_data["tg_id"],
            "subId": inbound_data["sub_id"],
            "reset": inbound_data["reset"]
        }
    ],
    "decryption": "none",
    "fallbacks": []
})

    stream_settings = json.dumps({
    "network": inbound_data["network"],
    "security": inbound_data["security"],
    "realitySettings": {
        "dest": inbound_data["dest"],
        "serverNames": inbound_data["server_names"],
        "privateKey": inbound_data["private_key"],
        "shortIds" : inbound_data["short_ids"],
        "settings": {
            "fingerprint": inbound_data["fingerprint"],
            "publicKey": inbound_data["public_key"],
            "spiderX" : inbound_data["spiderx"]
        }
    },
    "tcpSettings": {
        "acceptProxyProtocol": False,
        "header": {
            "type": "none"
        }
    }
})
    

    sniffing = json.dumps({
    "enabled": True,
    "destOverride": [
        "http",
        "tls",
        "quic",
        "fakedns"
    ],
    "metadataOnly": False,
    "routeOnly": False
})
    
    data = json.dumps({
    "up": inbound_data["up"],
    "down": inbound_data["down"],
    "total": inbound_data["total"],
    "remark": inbound_data["remark"],
    "enable": inbound_data["enable"],
    "expiryTime": inbound_data["expiryTime"],
    "listen": inbound_data["listen"],
    "port": inbound_data["port"],
    "protocol": inbound_data["protocol"],
    # Три нижних параметра пришлось вынести отдельно для двойного энкодинга, тк конкретно в случае vless это является необходимостью
    "settings": settings,
    "streamSettings": stream_settings,
    "sniffing": sniffing
})
    
    endpoints = inbound_data["endpoints"]
    auth_headers = inbound_data["auth_headers"]

    r = await http(method="POST", url = webpath + endpoints["add_inbound"], data=data, headers=auth_headers)
    print(r.status_code)
#--------------------------------------------------------------------------

#|=============================[Add Inbound Init]=============================|
async def add_inbound(auth_headers, webpath):
    r = await http(method="POST", url = webpath + endpoints["keygen"], headers=auth_headers)
    keys = r.json()['obj']

    up = 0
    down = 0
    total = 0
    remark = await generator_func.string_generator(type="letter", lenght=8)
    enable = True
    expiryTime = 0
    listen = ""
    port = random.randint(1000, 65535)
    protocol = "vless"
    client_id = str(uuid.uuid4())
    email = await generator_func.string_generator(type="letter", lenght=8)
    limit_ip = 0
    total_gb = 0
    client_expiry_time = 0
    tg_id = ""
    sub_id = await generator_func.string_generator(type="letdiggest", lenght=17)
    reset = 0
    network = "tcp"
    security = "reality"
    dest = "yahoo.com:443"
    server_names = [
    "yahoo.com",
    "www.yahoo.com"
    ]
    short_ids = await generator_func.random_short_ids()
    private_key = keys["privateKey"]
    public_key = keys["publicKey"]
    fingerprint = "random"
    spiderx = "/"

#Заворачивание всех переменных в единый словарь
    inbound_data = {
        "endpoints" : endpoints,
        "auth_headers" : auth_headers,
        "up" : up,
        "down" : down,
        "total" : total,
        "remark" : remark,
        "enable" : enable,
        "expiryTime" : expiryTime,
        "listen" : listen,
        "port" : port,
        "protocol" : protocol,
        "client_id" : client_id,
        "email" : email,
        "limit_ip" : limit_ip,
        "total_gb" : total_gb,
        "client_expiry_time" : client_expiry_time,
        "tg_id" : tg_id,
        "sub_id" : sub_id,
        "reset" : reset,
        "network" : network,
        "security" : security,
        "dest" : dest,
        "server_names" : server_names,
        "short_ids" : short_ids,
        "private_key" : private_key,
        "public_key" : public_key,
        "fingerprint" : fingerprint,
        "spiderx" : spiderx,
    }
    if os.path.exists("qr_code"):
        r = await generator_func.create_config(inbound_data, webpath)
        return await add_inbound_data(inbound_data), r
    else:
        os.makedirs("qr_code")
        r = await generator_func.create_config(inbound_data)
        return await add_inbound_data(inbound_data, webpath), r
#--------------------------------------------------------------------------
#|=============================[Add Inbound Init]=============================|
async def geo_ip(hostname):
    r = await http(url = "http://ip-api.com/json/" + hostname)
    return str(r.json()["country"])
#--------------------------------------------------------------------------