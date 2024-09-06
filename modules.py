import json
from config import http, endpoints
import random, uuid
from string import ascii_letters, digits



ascii_letdigest = ascii_letters + digits

async def login(username, password): # DONE

    auth_data = {
        'username': username,
        'password': password
    }

    r = await http(method="POST", url=endpoints["base_path"] + endpoints["login"] , data=auth_data)
    session_cookie = r.cookies.get("3x-ui")

    if session_cookie:
        print(f"Login successful")

    headers = {
            "Accept": "application/json",
            "Cookie": f"3x-ui={session_cookie}"  # Добавляем куку в заголовки запроса
        }
    if r is None:
        return None
    else:
        return headers



async def get_list(auth_headers):
    r = await http(url = endpoints["base_path"] + endpoints["list"], headers=auth_headers)
    remarks = r.json()["obj"]
    counter = 0
    for id in remarks:
        counter += 1
        print(f"[{counter}]{id['remark']}")

async def get_inbound(auth_headers):
    r = await http(url = endpoints["base_path"] + endpoints["get_inbound"] + "1", headers=auth_headers)
    remarks = r.json()["obj"]
    print(remarks)

async def delete_inbound(auth_headers):
    r = await http(url = endpoints["base_path"] + endpoints["delete_inbound"] + "/1", headers=auth_headers)
    print(r)

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

async def add_inbound_data(inbound_data):
    data = {
        "up": inbound_data["up"],
        "down": inbound_data["down"],
        "total": inbound_data["total"],
        "remark": inbound_data["remark"],
        "enable": inbound_data["enable"],
        "expiryTime": inbound_data["expiryTime"],
        "listen": inbound_data["listen"],
        "port": inbound_data["port"],
        "protocol": inbound_data["protocol"],
        "settings": {
            "clients": [
                {
                    "id": inbound_data["client_id"],
                    "flow": "",
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
        },
        "streamSettings": {
            "network": inbound_data["network"],
            "security": inbound_data["security"],
            "externalProxy": [],
            "realitySettings": {
                "show": False,
                "xver": 0,
                "dest": inbound_data["dest"],
                "serverNames": inbound_data["server_names"],
                "privateKey": inbound_data["private_key"],
                "minClient": "",
                "maxClient": "",
                "maxTimediff": 0,
                "shortIds": inbound_data["short_ids"],
                "settings": {
                    "publicKey": inbound_data["public_key"],
                    "fingerprint": inbound_data["fingerprint"],
                    "serverName": "",
                    "spiderX": inbound_data["spider_x"]
                }
            },
            "tcpSettings": {
                "acceptProxyProtocol": False,
                "header": {
                    "type": "none"
                }
            }
        },
        "sniffing": {
            "enabled": False,
            "destOverride": ["http", "tls", "quic", "fakedns"],
            "metadataOnly": False,
            "routeOnly": False
        }
    }
    
    endpoints = inbound_data["endpoints"]
    auth_headers = inbound_data["auth_headers"]

    r = await http(method="POST", url = endpoints["base_path"] + endpoints["add_inbound"], json=data, headers=auth_headers)
    print(r)


async def add_inbound(auth_headers):
    r = await http(method="POST", url = endpoints["base_path"] + endpoints["keygen"], headers=auth_headers)
    keys = r.json()['obj']

    up = 0
    down = 0
    total = 0
    remark = "huhuhuhuhu"
    enable = True
    expiryTime = 0
    listen = ""
    port = random.randint(1000, 65535)
    protocol = "vless"
    client_id = str(uuid.uuid4())
    email = str()
    limit_ip = 0
    total_gb = 0
    client_expiry_time = 0
    tg_id = ""
    sub_id = str()
    reset = 0
    network = "tcp"
    security = "reality"
    dest = "yahoo.com:443"
    server_names = [
    "yahoo.com",
    "www.yahoo.com"
    ],
    private_key = keys["privateKey"]
    short_ids = [
    "12",
    "73a21a72b0",
    "533716fa",
    "818e07ab59c4fc",
    "8c93",
    "a3bf36",
    "df114f8d28ce94d2",
    "1bcad2b1873a"
    ]
    public_key = keys["publicKey"]
    fingerprint = "random"
    spider_x = "/"

    for i in range(1, 8):
        email += ascii_letters[random.randint(1, 50)]
        pass
    for i in range(1, 17):
        sub_id += ascii_letdigest[random.randint(1, 60)]

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
        "private_key" : private_key,
        "short_ids" : short_ids,
        "public_key" : public_key,
        "fingerprint" : fingerprint,
        "spider_x" : spider_x,
    }

    return await add_inbound_data(inbound_data)



#generate_config = config_generator("vless", config, data)