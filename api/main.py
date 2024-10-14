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
# 1. /user/create
@app.post("/user/create", tags=[Tags.user], summary="Register user")
async def user_create(data = Body(example=ex.user_create)):
    r = await api.user_create(data)
    return r
#--------------------------------------------------------------------------

# 2. /user/{tgid}
@app.get("/user/{tgid}", tags=[Tags.user], summary="User info")
async def user_info(tgid: int):
    r = await api.user_info(tgid)
    return r
#--------------------------------------------------------------------------

# 3. /user/agree/{tgid}
@app.get("/user/agree/{tgid}", tags=[Tags.user], summary="User agree")
async def user_info(tgid: int):
    r = await api.agree(tgid)
    return r
#--------------------------------------------------------------------------

# 4. /user/check_voucher
@app.post("/user/check_voucher", tags=[Tags.user], summary="Voucher check")
async def check_voucher(data = Body(example=ex.user_create)):
    r = await api.check_voucher(data)
    return r
#--------------------------------------------------------------------------

# 5. /user/activate_voucher
@app.post("/user/activate_voucher", tags=[Tags.user], summary="Voucher activate")
async def activate_voucher(data = Body(example=ex.user_create)):
    r = await api.activate_voucher(data)
    return r
#--------------------------------------------------------------------------

# 6. /user/get_subscription/{tgid}
@app.get("/user/get_subscription/{tgid}", tags=[Tags.user], summary="Get subscription")
async def get_subscription(tgid: int):
    r = await api.get_subscription(tgid)
    return r
#--------------------------------------------------------------------------

# 7. /user/set_language
@app.post("/user/set_language", tags=[Tags.user], summary="Set language")
async def set_language(json = Body(example=ex.set_language)):
    r = await api.set_language(json)
    return r
#--------------------------------------------------------------------------

# 8. /user/check_language/{tgid}
@app.get("/user/check_language/{tgid}", tags=[Tags.user], summary="Check language")
async def check_language(tgid: int):
    r = await api.check_language(tgid)
    return r
#--------------------------------------------------------------------------

# 9. /user/config_limit/{tgid}
@app.get("/user/config_limit/{tgid}", tags=[Tags.user], summary="Check config limit")
async def config_limit(tgid: int):
    r = await api.config_limit(tgid)
    return r
#--------------------------------------------------------------------------

# 10. /user/reduce_config_limit/{tgid}
@app.get("/user/reduce_config_limit/{tgid}", tags=[Tags.user], summary="reduce config limit")
async def reduce_config_limit(tgid: int):
    r = await api.reduce_config_limit(tgid)
    return r
#--------------------------------------------------------------------------

# 11. /user/restore_config_limit/{tgid}
@app.get("/user/restore_config_limit/{hostname}", tags=[Tags.user], summary="restore config limit")
async def restore_config_limit(hostname: str):
    r = await api.restore_config_limit(hostname)
    return r
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
#|=============================[End User routes]=============================|

#|=============================[Admin routes]=============================|
# 1. /admin/isadmin/{tgid}
@app.get("/admin/isadmin/{tgid}", tags=[Tags.admin], summary="Is admin")
async def is_admin(tgid: int):
    r = await api.is_admin(tgid)
    return r
#--------------------------------------------------------------------------

# 2. /admin/ban/{tgid}
@app.get("/admin/ban/{tgid}", tags=[Tags.admin], summary="Set admin")
async def admin_ban(tgid: int):
    r = await api.admin_ban(tgid)
    return r
#--------------------------------------------------------------------------

# 3. /admin/unban/{tgid}
@app.get("/admin/unban/{tgid}", tags=[Tags.admin], summary="Ban user")
async def admin_unban(tgid: int):
    r = await api.admin_unban(tgid)
    return r
#--------------------------------------------------------------------------

# 4. /admin/fetchadmins
@app.get("/admin/fetchadmins", tags=[Tags.admin], summary="Get all users")
async def admin_fetchadmins():
    r = await api.admin_fetchadmins()
    return r
#--------------------------------------------------------------------------

# 5. /admin/voucherone
@app.get("/admin/voucher_one", tags=[Tags.admin], summary="Create 1 month voucher")
async def admin_create_voucher_one():
    r = await api.admin_create_voucher_one()
    return r
#--------------------------------------------------------------------------

# 6. /admin/vouchersix
@app.get("/admin/voucher_six", tags=[Tags.admin], summary="Create 6 month voucher")
async def admin_create_voucher_six():
    r = await api.admin_create_voucher_six()
    return r
#--------------------------------------------------------------------------

# 7. /admin/voucheryear
@app.get("/admin/voucher_year", tags=[Tags.admin], summary="Create year voucher")
async def admin_create_voucher_year():
    r = await api.admin_create_voucher_year()
    return r
#--------------------------------------------------------------------------

#|=============================[xui routes]=============================|
# 1. /xui/init_server
@app.post("/xui/init_server", tags=[Tags.x_ui], summary="server initialization")
async def init_server(dict = Body(example=ex.init_server)):
    r = await api.init_server(dict)
    return r
#--------------------------------------------------------------------------
# 2. /xui/xui_login
@app.post("/xui/xui_login", tags=[Tags.x_ui], summary="xui login")
async def xui_login(json = Body(example=ex.xui_login)):
    r = await api.xui_login(json)
    return r
#--------------------------------------------------------------------------
# 3. /xui/inbound_creation
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
# 4. /xui/servers_count
@app.get("/xui/servers_count", tags=[Tags.x_ui], summary="servers_count")
async def servers_count():
    r = await api.servers_count()
    return r
#--------------------------------------------------------------------------
# 5. /xui/server_info/{hostname}
@app.get("/xui/server_info/{hostname}", tags=[Tags.x_ui], summary="servers_count")
async def server_info(hostname: str):
    decoded_hostname = urllib.parse.unquote(hostname)
    r = await api.server_info(decoded_hostname)
    return r
#--------------------------------------------------------------------------
# 6. /xui/remove_configs/{hostname}
@app.get("/xui/remove_configs/{hostname}", tags=[Tags.x_ui], summary="remove_configs")
async def remove_configs(hostname: str):
    r = await api.remove_configs(hostname)
    return r
#--------------------------------------------------------------------------

#|=============================[servers routes]=============================|
# 1. /servers/add_server
@app.post("/servers/add_server", tags=[Tags.servers], summary="add server")
async def add_server(dict = Body(example=ex.add_server)):
    r = await api.add_server(dict)
    return r
#--------------------------------------------------------------------------

# 2. /servers/get_servers
@app.get("/servers/get_servers", tags=[Tags.servers], summary="get server")
async def add_server():
    r = await api.get_servers()
    return r
#--------------------------------------------------------------------------

# 3. /servers/server_down
@app.post("/servers/server_down", tags=[Tags.servers], summary="disable server")
async def server_down(dict = Body(example=ex.server_down)):
    r = await api.server_down(dict)
    return r
#--------------------------------------------------------------------------

#|=============================[CryptoBot routes]=============================|
# 1. /cryptobot/getMe
@app.get("/cryptobot/getMe", tags=[Tags.cryptobot], summary="test token")
async def getMe():
    r = await api.getMe()
    return r
#--------------------------------------------------------------------------

# 2. /cryptobot/create_invoice
@app.post("/cryptobot/create_invoice", tags=[Tags.cryptobot], summary="test token")
async def create_invoice(dict = Body(ex.create_invoice)):
    r = await api.create_invoice(dict)
    return r
#--------------------------------------------------------------------------

# 3. /cryptobot/check_invoice
@app.post("/cryptobot/check_invoice", tags=[Tags.cryptobot], summary="test token")
async def check_invoice():
    r = await api.check_invoice()
    return r
#--------------------------------------------------------------------------

# 4. /cryptobot/get_invoices
@app.get("/cryptobot/get_invoices", tags=[Tags.cryptobot], summary="get invoices")
async def get_invoices():
    r = await api.get_invoices()
    return r
#--------------------------------------------------------------------------

# 4. /cryptobot/paid_invoices/{invoice_id}
@app.get("/cryptobot/paid_invoices/{invoice_id}", tags=[Tags.cryptobot], summary="paid invoices")
async def paid_invoices(invoice_id: int):
    r = await api.paid_invoices(invoice_id)
    return r
#--------------------------------------------------------------------------

# 4. /cryptobot/paid_invoices/{invoice_id}
@app.get("/cryptobot/expired_invoices/{invoice_id}", tags=[Tags.cryptobot], summary="expired invoices")
async def expired_invoices(invoice_id: int):
    r = await api.expired_invoices(invoice_id)
    return r
#--------------------------------------------------------------------------

# 4. /cryptobot/update_subscription
@app.get("/cryptobot/update_subscription/{invoice_id}", tags=[Tags.cryptobot], summary="update subscription")
async def update_subscription(invoice_id: int):
    r = await api.update_subscription(invoice_id)
    return r


#|=============================[redis routes]=============================|
# 1. /redis_get_all
@app.get("/redis_get_all", tags=[Tags.x_ui], summary="inbound creation")
async def redis_get_all():
    r = await api.redis_get_all()
    return r
#--------------------------------------------------------------------------



