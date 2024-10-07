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
@app.post("/user/checkvoucher", tags=[Tags.user], summary="Voucher check")
async def checkvoucher(data = Body(example=ex.user_create)):
    r = await api.checkvoucher(data)
    return r
#--------------------------------------------------------------------------
@app.post("/user/activatevoucher", tags=[Tags.user], summary="Voucher activate")
async def activate_voucher(data = Body(example=ex.user_create)):
    r = await api.activate_voucher(data)
    return r
#--------------------------------------------------------------------------
#|=============================[End User routes]=============================|

#|=============================[Admin routes]=============================|
@app.get("/admin/isadmin/{tgid}", tags=[Tags.admin], summary="Is admin")
async def is_admin(tgid: int):
    r = await api.is_admin(tgid)
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
@app.get("/admin/fetchadmins", tags=[Tags.admin], summary="Get all users")
async def admin_fetchadmins():
    r = await api.admin_fetchadmins()
    return r
#--------------------------------------------------------------------------
@app.get("/admin/voucherone", tags=[Tags.admin], summary="Create 1 month voucher")
async def admin_create_voucher_one():
    r = await api.admin_create_voucher_one()
    return r
#--------------------------------------------------------------------------
@app.get("/admin/vouchersix", tags=[Tags.admin], summary="Create 6 month voucher")
async def admin_create_voucher_six():
    r = await api.admin_create_voucher_six()
    return r
#--------------------------------------------------------------------------
@app.get("/admin/voucheryear", tags=[Tags.admin], summary="Create year voucher")
async def admin_create_voucher_year():
    r = await api.admin_create_voucher_year()
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
@app.get("/xui/remove_configs/{hostname}", tags=[Tags.x_ui], summary="remove_configs")
async def remove_configs(hostname: str):
    r = await api.remove_configs(hostname)
    return r
#--------------------------------------------------------------------------
@app.post("/servers/add_server", tags=[Tags.servers], summary="add server")
async def add_server(dict = Body(example=ex.add_server)):
    r = await api.add_server(dict)
    return r
#--------------------------------------------------------------------------
@app.get("/servers/get_servers", tags=[Tags.servers], summary="get server")
async def add_server():
    r = await api.get_servers()
    return r
#--------------------------------------------------------------------------
@app.post("/servers/server_down", tags=[Tags.servers], summary="disable server")
async def server_down(dict = Body(example=ex.server_down)):
    r = await api.server_down(dict)
    return r
#--------------------------------------------------------------------------
@app.get("/redis_get_all", tags=[Tags.x_ui], summary="inbound creation")
async def redis_get_all():
    r = await api.redis_get_all()
    return r
#--------------------------------------------------------------------------



