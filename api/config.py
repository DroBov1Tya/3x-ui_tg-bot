from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from fastapi import FastAPI
from enum import Enum
import httpx
import asyncpg
from env import debug, apikey, pg_conn


# VARS #
debug = debug               # TURN OFF DEBUG ON PROD !!!
SECRET_VALUE = apikey       # CHANGE ME ON PROD !!!
SECRET_HEADER = 'X-API-Key'


docs_title = 'Duck Say Crack API'
docs_description = 'Не лезь, убьёт!'

class Tags(Enum):
    user = "User"
    temp_mail = "Temp mail"
    admin = "Admin"


def auth401():
    X_API_KEY = APIKeyHeader(name=SECRET_HEADER)

    def api_key_auth(x_api_key: str = Depends(X_API_KEY)):
        if x_api_key != SECRET_VALUE:
            raise HTTPException(status_code=401)

    auth_dep = [Depends(api_key_auth)]
    return auth_dep

def api_init():
    if debug:
        app = FastAPI(
            #dependencies = auth401(),
            title = docs_title,
            description = docs_description,
            )
    else:
        app = FastAPI(
            docs_url = None, # Disable docs (Swagger UI)
            redoc_url = None, # Disable redoc
            dependencies = auth401(),
            title = docs_title,
            description = docs_description,
        )
    return app

# asyncpg wrapper

class PostgreSQL():
    def __init__(self):
        self.pool = None

    async def connect(self):
        if self.pool is None:
            self.pool = await asyncpg.create_pool(pg_conn)
            return self

    async def disconnect(self):
        if self.pool is not None:
            await self.pool.close()

    async def execute(self, query: str, args = ()):
        await self.connect()

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(query, *args)

    async def fetch(self, query: str, args = (), count: int = 1, cache: bool = False):
        await self.connect()

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                cursor = await connection.cursor(query, *args)
                response = await cursor.fetch(count)

                if count == 1 and len(response) > 0:
                    return dict(response[0])

                return response if len(response) > 0 else None

    async def fetchall(self, query: str, args = ()):
        await self.connect()
        
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                return await connection.fetch(query, *args)

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