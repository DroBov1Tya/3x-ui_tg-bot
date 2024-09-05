import json
from config import http
import asyncio
import config_generator
import urllib
import random, uuid
from string import ascii_letters, digits

ascii_letdigest = ascii_letters + digits

async def login(endpoints, data):
    r = await http(method="POST", url=endpoints["base_path"] + endpoints["login"] , data=data, cookie=True)
    session_cookie = r.get("3x-ui")
    print(r.get("3x-ui"))
    if session_cookie:
        print(f"Login successful, session cookie: {session_cookie}")

    headers = {
            "Accept": "application/json",
            "Cookie": f"3x-ui={session_cookie}"  # Добавляем куку в заголовки запроса
        }
    if r is None:
        return None
    else:
        return headers

async def get_list(endpoints, data):
    headers = await login(endpoints, data)
    r = await http(url = endpoints["base_path"] + endpoints["list"], headers=headers)
    remarks = r["obj"]
    counter = 0
    for id in remarks:
        counter += 1
        print(f"[{counter}]{id['remark']}")

async def get_inbound(endpoints, data):
    headers = await login(endpoints, data)
    r = await http(url = endpoints["base_path"] + endpoints["get_inbound"] + "1", headers=headers)
    remarks = r["obj"]
    print(remarks)

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

async def add_inbound_data(
    up: int, down: int, total: int, remark: str, enable: bool, expiry_time: int, 
    listen: str, port: int, protocol: str, client_id: str, email: str, 
    limit_ip: int, total_gb: int, client_expiry_time: int, tg_id: str, sub_id: str, 
    reset: int, network: str, security: str, dest: str, server_names: list, 
    private_key: str, short_ids: list, public_key: str, fingerprint: str, spider_x: str, 
    endpoints: dict, headers: str
):
    data = {
        "up": up,
        "down": down,
        "total": total,
        "remark": remark,
        "enable": enable,
        "expiryTime": expiry_time,
        "listen": listen,
        "port": port,
        "protocol": protocol,
        "settings": {
            "clients": [
                {
                    "id": client_id,
                    "flow": "",
                    "email": email,
                    "limitIp": limit_ip,
                    "totalGB": total_gb,
                    "expiryTime": client_expiry_time,
                    "enable": enable,
                    "tgId": tg_id,
                    "subId": sub_id,
                    "reset": reset
                }
            ],
            "decryption": "none",
            "fallbacks": []
        },
        "streamSettings": {
            "network": network,
            "security": security,
            "externalProxy": [],
            "realitySettings": {
                "show": False,
                "xver": 0,
                "dest": dest,
                "serverNames": server_names,
                "privateKey": private_key,
                "minClient": "",
                "maxClient": "",
                "maxTimediff": 0,
                "shortIds": short_ids,
                "settings": {
                    "publicKey": public_key,
                    "fingerprint": fingerprint,
                    "serverName": "",
                    "spiderX": spider_x
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
    
    r = await http(method="POST", url = endpoints["base_path"] + endpoints["add_inbound"], data=data, headers=headers)
    print(r)
    
# async def split_uuid_to_short_ids(uuid_str):
#     clean_uuid = uuid_str.replace("-", "")
#     short_ids = [
#         clean_uuid[:16],     # Первая часть из 16 символов
#         clean_uuid[16:30],   # Вторая часть из 14 символов
#         clean_uuid[30:43],   # Третья часть из 13 символов
#         clean_uuid[43:53],   # Четвертая часть из 10 символов
#         clean_uuid[53:57],   # Пятая часть из 4 символов
#         clean_uuid[57:59],   # Шестая часть из 2 символов
#         clean_uuid[59:67],   # Седьмая часть из 8 символов
#         clean_uuid[67:75]    # Восьмая часть из 8 символов
#     ]
    
#     return short_ids

async def add_inbound(endpoints, data):
    headers = await login(endpoints, data)
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
    enable = "true"
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
    private_key = str()
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
    public_key = str()
    fingerprint = "random"
    spider_x = "/"

    for i in range(1, 8):
        email += ascii_letters[random.randint(1, 50)]
        pass
    for i in range(1, 17):
        sub_id += ascii_letdigest[random.randint(1, 60)]
    for i in range(1, 44):
        private_key += ascii_letdigest[random.randint(1, 60)]
        public_key += ascii_letdigest[random.randint(1, 60)]

    spider_x = "/"
    return await add_inbound_data(up, down, total, remark, enable, expiryTime, listen, port, protocol, client_id, email, limit_ip, total_gb, client_expiry_time, tg_id, sub_id, reset, network, security, dest, server_names, private_key, short_ids, public_key, fingerprint, spider_x, endpoints, headers)



#generate_config = config_generator("vless", config, data)