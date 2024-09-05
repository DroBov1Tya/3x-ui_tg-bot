from config import http
import asyncio
from pyxui import XUI
import json
import modules


endpoints = {
    "base_path" :                   "http://185.234.13.205:2053/4fGKZs4G0c",
    "login" :                       "/login",
    "list" :                        "/panel/api/inbounds/list",
    "get_inbound" :                 "/panel/api/inbounds/get/",
    "get_client" :                  "/panel/api/inbounds/getClientTraffics/{email}",
    "get_client_ip" :               "/panel/api/inbounds/clientIps/{email}",
    "add_inbound" :                 "/panel/api/inbounds/add",
    "add_client" :                  "/panel/api/inbounds/addClient",
    "update_inbound" :              "/panel/api/inbounds/update/{inboundId}",
    "update_client" :               "/panel/api/inbounds/updateClient/{uuid}",
    "reset_client_ip" :             "/panel/api/inbounds/clearClientIps/{email}",
    "reset_inbounds_stat" :         "/panel/api/inbounds/resetAllTraffics",
    "reset_inbound_clients_stat" :  "/panel/api/inbounds/resetAllClientTraffics/{inboundId}",
    "delete_inbound" :              "/panel/api/inbounds/del/{inboundId}",
    "delete_client" :               "/panel/api/inbounds/{inboundId}/delClient/{uuid}",
    "delete_depleted_dlients" :     "/panel/api/inbounds/delDepletedClients/{inboundId}",
    "online_clients" :              "/panel/api/inbounds/onlines",
    "export_database" :             "/panel/api/inbounds/createbackup"
    }





async def create_client():
    r = await modules.add_client(
        inbound_id=1,
        email="y84nsnqw3",
        uuid="5ff65536-37e2-4d34-aa1f-e460dd037f12",
        endpoints = dict(endpoints),
        data = dict(data),
        enable = True,
        flow = "",
        limit_ip = 0,
        total_gb = 0,
        expire_time = 0, # You must pass 13 digit timestamp
        telegram_id = "",
        subscription_id = ""
    )

config2 = {
    "ps": "Staliox-Me",
    "add": "staliox.com",
    "port": "443",
    "id": "a85def57-0a86-43d1-b15c-0494519067c6"
}

data2 = {
    "security": "tls",
    "type": "ws",
    "host": "staliox.site",
    "path": "/",
    "sni": "staliox.site",
    "alpn": "h2,http/1.1",
    "fp": "chrome"
}

#generate_config = modules.config_generator("vless", config, data)



async def main():
    endpoints = {
    "base_path" :                   "http://185.234.13.205:2053/4fGKZs4G0c",
    "login" :                       "/login",
    "list" :                        "/panel/api/inbounds/list",
    "get_inbound" :                 "/panel/api/inbounds/get/",
    "get_client" :                  "/panel/api/inbounds/getClientTraffics/{email}",
    "get_client_ip" :               "/panel/api/inbounds/clientIps/{email}",
    "add_inbound" :                 "/panel/api/inbounds/add",
    "add_client" :                  "/panel/api/inbounds/addClient",
    "update_inbound" :              "/panel/api/inbounds/update/{inboundId}",
    "update_client" :               "/panel/api/inbounds/updateClient/{uuid}",
    "reset_client_ip" :             "/panel/api/inbounds/clearClientIps/{email}",
    "reset_inbounds_stat" :         "/panel/api/inbounds/resetAllTraffics",
    "reset_inbound_clients_stat" :  "/panel/api/inbounds/resetAllClientTraffics/{inboundId}",
    "delete_inbound" :              "/panel/api/inbounds/del/{inboundId}",
    "delete_client" :               "/panel/api/inbounds/{inboundId}/delClient/{uuid}",
    "delete_depleted_dlients" :     "/panel/api/inbounds/delDepletedClients/{inboundId}",
    "online_clients" :              "/panel/api/inbounds/onlines",
    "export_database" :             "/panel/api/inbounds/createbackup"
    }
    data = {
        'username':'d2nNd1Ha',
        'password':'omCOLPrE'
        }
    #await modules.get_inbound(endpoints, data)
    await modules.get_list(endpoints, data)
    #await create_client()
    #await modules.add_inbound(endpoints, data)
asyncio.run(main()) 
