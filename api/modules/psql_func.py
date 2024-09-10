from config import PostgreSQL

pg = PostgreSQL()
async def test():
    pipikaka = "zalupa"
    ssa = "asas"
    await pg.fetch("SELECT user FROM testtable WHERE id = $1 and name = $2", (pipikaka, ssa))



async def userinfo(data):
    userinfo = data['user']

    tgid, nickname, first_name, last_name = userinfo['tgid'], userinfo['nickname'], userinfo['first_name'], userinfo['last_name']
    str = f"INSERT INTO users (tgid, nickname, first_name, last_name, is_banned) VALUES ({tgid}, '{nickname}', '{first_name}', '{last_name}', True) ON CONFLICT (tgid) DO NOTHING RETURNING true;"
    return str