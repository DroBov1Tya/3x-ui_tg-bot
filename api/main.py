import api
import base64
import urllib.parse
from fastapi import Body, UploadFile
from config import api_init, Tags
from examples import ex
from fastapi.responses import FileResponse
# pre-config #
app = api_init()

# routes #
#|=============================[User routes]=============================|
# 1. /user/
@app.post("/user/create", tags=[Tags.user], summary="Register user")
async def user_create(data = Body(example=ex.user_create)):
    r = await api.user_create(data)
    return r
#--------------------------------------------------------------------------
@app.get("/user/{tgid}", tags=[Tags.user], summary="User info")
async def user_info(tgid: int):
    r = await api.user_info(tgid)
    return r
#--------------------------------------------------------------------------

#|=============================[End User routes]=============================|

#|=============================[Admin routes]=============================|
@app.get("/admin/isadmin/{tgid}", tags=[Tags.admin], summary="Is admin")
async def is_admin(tgid: int):
    r = await api.is_admin(tgid)
    return r
#--------------------------------------------------------------------------
@app.get("/admin/set/{tgid}", tags=[Tags.admin], summary="Level check")
async def admin_set(tgid: int):
    r = await api.admin_set(tgid)
    return r
#--------------------------------------------------------------------------
@app.get("/admin/unset/{tgid}", tags=[Tags.admin], summary="Level check")
async def admin_set(tgid: int):
    r = await api.admin_unset(tgid)
    return r
#--------------------------------------------------------------------------
@app.post("/admin/balance/", tags=[Tags.admin], summary="Level set")
async def admin_balance(tgid: int):
    r = await api.admin_balance(tgid)
    return r
#--------------------------------------------------------------------------
@app.get("/admin/ban/{tgid}", tags=[Tags.admin], summary="Set admin")
async def admin_ban(tgid: int):
    r = await api.admin_ban(tgid)
    return r
#--------------------------------------------------------------------------
@app.get("/admin/unban/{tgid}", tags=[Tags.admin], summary="Ban user")
async def admin_unban(tgid: int):
    r = await api.admin_unban(tgid)
    return r
#--------------------------------------------------------------------------
@app.get("/admin/level1/{tgid}", tags=[Tags.admin], summary="Unban user")
async def admin_level1(tgid: int):
    r = await api.admin_level1(tgid)
    return r
#--------------------------------------------------------------------------
@app.get("/admin/level2/{tgid}", tags=[Tags.admin], summary="Get user")
async def admin_level2(tgid: int):
    r = await api.admin_level2(tgid)
    return r
#--------------------------------------------------------------------------
@app.get("/admin/level3/{tgid}", tags=[Tags.admin], summary="Get all users")
async def admin_level3(tgid: int):
    r = await api.admin_level3(tgid)
    return r
#--------------------------------------------------------------------------
@app.get("/admin/grepusers", tags=[Tags.admin], summary="Get all users")
async def admin_grep_users(tgid: int):
    r = await api.admin_grep_users(tgid)
    return r
#--------------------------------------------------------------------------
@app.get("/admin/fetchadmins", tags=[Tags.admin], summary="Get all users")
async def admin_fetchadmins():
    r = await api.admin_fetchadmins()
    return r
#--------------------------------------------------------------------------
@app.post("/add_server", tags=[Tags.x_ui], summary="add server")
async def add_server(dict = Body(example=ex.add_server)):
    r = await api.add_server(dict)
    return r
#--------------------------------------------------------------------------
@app.post("/xui/init_server", tags=[Tags.x_ui], summary="server initialization")
async def init_server(dict = Body(example=ex.init_server)):
    r = await api.init_server(dict)
    return r
#--------------------------------------------------------------------------
@app.post("/xui/xui_login", tags=[Tags.x_ui], summary="xui login")
async def xui_login(json = Body(example=ex.xui_login)):
    r = await api.xui_login(json)
    return r
#--------------------------------------------------------------------------
@app.post("/xui/inbound_creation", tags=[Tags.x_ui], summary="inbound creation")
async def inbound_creation(json = Body(example=ex.inbound_creation)):
    print("Inbound creation handled")
    r = await api.inbound_creation(json)
    return r
    # qr = base64.b64decode(r["qr_data"])
    # with open("./qr_code/qr_image.png", "rb") as image_file:
    #     image_file.write(qr)
    #     qr_file = FileResponse(f"./qr_code/qr_image.png", media_type='application/octet-stream', filename=f"qr_image.png")
    #     return qr_file
#--------------------------------------------------------------------------
@app.get("/xui/servers_count", tags=[Tags.x_ui], summary="servers_count")
async def servers_count():
    r = await api.servers_count()
    return r
#--------------------------------------------------------------------------
@app.get("/xui/server_info/{hostname}", tags=[Tags.x_ui], summary="servers_count")
async def server_info(hostname: str):
    decoded_hostname = urllib.parse.unquote(hostname)
    r = await api.server_info(decoded_hostname)
    return r
#--------------------------------------------------------------------------
@app.get("/redis_get_all", tags=[Tags.x_ui], summary="inbound creation")
async def redis_get_all():
    r = await api.redis_get_all()
    return r
#--------------------------------------------------------------------------



