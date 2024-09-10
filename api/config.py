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


endpoints = {
    "base_path" :                   "http://191.96.235.118:2053/jJyuPk5b1F",
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
    "delete_inbound" :              "/panel/api/inbounds/del/",
    "delete_client" :               "/panel/api/inbounds/{inboundId}/delClient/{uuid}",
    "delete_depleted_dlients" :     "/panel/api/inbounds/delDepletedClients/{inboundId}",
    "online_clients" :              "/panel/api/inbounds/onlines",
    "export_database" :             "/panel/api/inbounds/createbackup",
    "keygen" :                      "/server/getNewX25519Cert"
    }