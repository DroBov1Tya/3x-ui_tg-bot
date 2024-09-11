from config import PostgreSQL
import json
from src import psql_func
from api.src import xui_func
from src import ssh_func
pg = PostgreSQL()

#--------------------------------------------------------------------------
# 1. /user/
async def user_create(data): # DONE
    sql = psql_func(data)
    r = await pg.fetch(sql)
    if r is None:
        return {"Success": False, "Reason": "User already exists"}
    else:
        return {"Success": True}
#--------------------------------------------------------------------------
# 2. /user/{tgid}
async def user_info(tgid): #DONE
    r = await pg.fetch(f"SELECT * FROM users WHERE tgid = {tgid};")
    if r is None:
        return {"Success": False, "Reason": "User not found"}
    else:
        return {"Success": True, "user": r }
#--------------------------------------------------------------------------
# 5. /user/isadmin
async def is_admin(tgid):
    r = await pg.fetch(f"SELECT is_admin FROM users WHERE tgid = {tgid};")
    if r['is_admin'] is False:
        return {"Success": False, "Reason": "User not admin"}
    else:
        return {"Success": True}
#--------------------------------------------------------------------------
# 9. /admin/
async def admin_set(tgid):
    r = await pg.fetch(f"UPDATE users SET is_admin = TRUE WHERE tgid = {tgid};")
    if not r['is_admin']:
        return {"Success": False, "Reason": "User not admin"}
    else:
        return {"Success": True}
#--------------------------------------------------------------------------
# 9. /admin/
async def admin_unset(tgid):
    r = await pg.fetch(f"UPDATE users SET is_admin = False WHERE tgid = {tgid};")
    if r is None:
        {"Success": False, "Reason": "User not found"}
    else:
        return {"Success": True, "result": r}
#--------------------------------------------------------------------------
# 10. /admin/
#async def admin_balance(tgid):
#--------------------------------------------------------------------------
# 11. /admin/
async def admin_ban(tgid):
    r = await pg.fetch(f"UPDATE users SET is_banned = TRUE WHERE tgid = {tgid};")
    if r is None:
        {"Success": False, "Reason": "User not found"}
    else:
        return {"Success": True, "result": r}
#--------------------------------------------------------------------------
# 12. /admin/
async def admin_unban(tgid):
    r = await pg.fetch(f"UPDATE users SET is_banned = FALSE WHERE tgid = {tgid};")
    if r is None:
        {"Success": False, "Reason": "User not found"}
    else:
        return {"Success": True, "result": r}
#--------------------------------------------------------------------------
# 13. /admin/
async def admin_level1(tgid):
    r = await pg.fetch(f"UPDATE users SET user_level = '1' WHERE tgid = {tgid};")
    if r is None:
        {"Success": False, "Reason": "User not found"}
    else:
        return {"Success": True, "result": r}
#--------------------------------------------------------------------------
# 14. /admin/
async def admin_level2(tgid):
    r = await pg.fetch(f"UPDATE users SET user_level = '2' WHERE tgid = {tgid};")
    if r is None:
        {"Success": False, "Reason": "User not found"}
    else:
        return {"Success": True, "result": r}
#--------------------------------------------------------------------------
# 15. /admin/
async def admin_level3(tgid):
    r = await pg.fetch(f"UPDATE users SET user_level = '3' WHERE tgid = {tgid};")
    if r is None:
        {"Success": False, "Reason": "User not found"}
    else:
        return {"Success": True, "result": r}
#--------------------------------------------------------------------------
# 16. /admin/
#async def admin_grep_user(data):
#--------------------------------------------------------------------------
# 17. /admin/
#async def admin_grep_users(data):
#--------------------------------------------------------------------------
async def admin_fetchadmins():
    r = await pg.fetchall(f"SELECT tgid FROM users WHERE is_admin = True")
    if r is None:
        {"Success": False, "Reason": "No found admins"}
    else:
        ids = []
        for admin in r:
            ids.append(admin['tgid'])
        return {"Success": True, "result": ids}
#--------------------------------------------------------------------------
async def xui_login():
    await xui_func.login()
#--------------------------------------------------------------------------
async def inbound_creation(username, password, path):
    auth_headers = await xui_func.login(username, password, path)
    await xui_func.add_inbound(auth_headers)
#--------------------------------------------------------------------------


