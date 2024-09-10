from config import PostgreSQL
import json
from modules import psql_func
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
# 3. /user/target/set
async def target_set(data):
    userinfo = data['user']
    tgid, target = userinfo['tgid'], userinfo['target']
    r = await pg.fetch(f"UPDATE users SET target = '{target}' WHERE tgid = {tgid};")
    if r is None:
        return {"Success": False, "Reason": "User not found"}
    else:
        return {"Success": True, "user": r }
#--------------------------------------------------------------------------
# 4. /user/target/get/{tgid}
async def target_get(tgid):
    r = await pg.fetch(f"SELECT target FROM users WHERE tgid = {tgid};")
    if r:
        return {"Success": True, "result": r }
    else:
        return {"Success": False, "Reason": "User not found"}
#--------------------------------------------------------------------------
# 5. /user/isadmin
async def is_admin(tgid):
    r = await pg.fetch(f"SELECT is_admin FROM users WHERE tgid = {tgid};")
    if r['is_admin'] is False:
        return {"Success": False, "Reason": "User not admin"}
    else:
        return {"Success": True}
#--------------------------------------------------------------------------
# 6. /tempmail/create
async def mail_create(data):
    userinfo = data['info']
    tgid, login, domain = userinfo['tgid'], userinfo['login'], userinfo['domain']
    r = await pg.fetch(f"INSERT INTO temp_mail (tgid, login, domain) VALUES ({tgid}, '{login}', '{domain}') ON CONFLICT (tgid) DO UPDATE SET login = '{login}', domain = '{domain}';")
    return {"Success": True}
#--------------------------------------------------------------------------
# 7. /tempmail/check/mailbox/{tgid}
async def mailbox_check(tgid):
    r = await pg.fetch(f"SELECT login, domain from temp_mail WHERE tgid = {tgid};")
    if r:
        return {"Success": True, "login": r['login'], "domain": r['domain'] }
    else:
        {"Success": False, "Reason": "User not found"}
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


