import api
from fastapi import Body, UploadFile
from config import api_init, Tags
from examples import ex
# pre-config #
app = api_init()

# routes #
#--------------------------------------------------------------------------
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
@app.post("/user/target/set", tags=[Tags.user], summary="Set target")
async def target_set(data = Body(example=ex.target_set)):
    r = await api.target_set(data)
    return r
#--------------------------------------------------------------------------
@app.get("/user/target/get/{tgid}", tags=[Tags.user], summary="Get target")
async def set_target(tgid: int):
    r = await api.target_get(tgid)
    return r
#--------------------------------------------------------------------------
@app.post("/tempmail/create", tags=[Tags.temp_mail], summary="Mail create")
async def mail_create(data = Body(example=ex.mail_create)):
    r = await api.mail_create(data)
    return r
#--------------------------------------------------------------------------
@app.get("/tempmail/check/mailbox/{tgid}", tags=[Tags.temp_mail], summary="Mailbox check")
async def mailbox_check(tgid: int):
    r = await api.mailbox_check(tgid)
    return r
#--------------------------------------------------------------------------
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



