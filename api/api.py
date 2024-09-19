import json
import logging
from config import PostgreSQL
from src import redis_func
from src import xui_func
from src import ssh_func
from typing import Dict, Any, Union

pg = PostgreSQL()
logger = logging.getLogger(__name__)

#|=============================[User panel]=============================|

#--------------------------------------------------------------------------
# 1. /user/
async def user_create(data: Dict[str, Any]) -> Dict[str, Any]: # DONE
    
    userinfo = data['user']
    tgid = userinfo['tgid']
    nickname = userinfo['nickname']
    first_name = userinfo['first_name']
    last_name = userinfo['last_name']


    query = """
        INSERT INTO users 
        (tgid, nickname, first_name, last_name, is_banned) 
        VALUES ($1, '$2', '$3', '$4', True) 
        ON CONFLICT (tgid) DO NOTHING RETURNING true;
    """
    values = [
        userinfo,
        tgid,
        nickname,
        first_name,
        last_name
    ]
    
    r = await pg.fetch(query,*values)

    if r is None:
        return {"Success": False, "Reason": "User already exists"}
    else:
        return {"Success": True}
#--------------------------------------------------------------------------

# 2. /user/{tgid}
async def user_info(tgid: str) -> Dict[str, Any]: #DONE
    query = """
        SELECT * FROM users WHERE tgid = $1;
    """
    
    r = await pg.fetch(query,tgid)

    if r is None:
        return {"Success": False, "Reason": "User not found"}
    else:
        return {"Success": True, "user": r }
#--------------------------------------------------------------------------

# 3. /user/isadmin
async def is_admin(tgid: str) -> Dict[str, Any]:
    query = """
        SELECT is_admin FROM users WHERE tgid = $1;
    """

    r = await pg.fetch(query, tgid)

    if r['is_admin'] is False:
        return {"Success": False, "Reason": "User not admin"}
    else:
        return {"Success": True}
#--------------------------------------------------------------------------

#|=============================[End User panel]=============================|

#|=============================[Admin panel]=============================|

# 1. /admin/
async def admin_set(tgid: str) -> Dict[str, Any]:

    query = """
        UPDATE users SET is_admin = TRUE WHERE tgid = $1;
    """

    r = await pg.fetch(query, tgid)

    if not r['is_admin']:
        return {"Success": False, "Reason": "User not admin"}
    else:
        return {"Success": True}
#--------------------------------------------------------------------------

# 2. /admin/
async def admin_unset(tgid: str) -> Dict[str, Any]:
    query = """
        UPDATE users SET is_admin = False WHERE tgid = $1;
    """

    r = await pg.fetch(query, tgid)

    if r is None:
        {"Success": False, "Reason": "User not found"}
    else:
        return {"Success": True, "result": r}
#--------------------------------------------------------------------------

# 3. /admin/
#async def admin_balance(tgid):
#--------------------------------------------------------------------------

# 4. /admin/
async def admin_ban(tgid: str) -> Dict[str, Any]:

    query = """
        
    """
    r = await pg.fetch(
        "UPDATE users SET is_banned = TRUE WHERE tgid = $1;", 
        tgid
    )
    if r is None:
        {"Success": False, "Reason": "User not found"}
    else:
        return {"Success": True, "result": r}
#--------------------------------------------------------------------------

# 5. /admin/
async def admin_unban(tgid: str) -> Dict[str, Any]:
    r = await pg.fetch(
        "UPDATE users SET is_banned = FALSE WHERE tgid = $1;", 
        tgid
    )
    if r is None:
        {"Success": False, "Reason": "User not found"}
    else:
        return {"Success": True, "result": r}
#--------------------------------------------------------------------------

# 6. /admin/
async def admin_level1(tgid: str) -> Dict[str, Any]:
    r = await pg.fetch(
        "UPDATE users SET user_level = '1' WHERE tgid = $1;", 
        tgid
    )
    if r is None:
        {"Success": False, "Reason": "User not found"}
    else:
        return {"Success": True, "result": r}
#--------------------------------------------------------------------------

# 7. /admin/
async def admin_level2(tgid: str) -> Dict[str, Any]:
    r = await pg.fetch(
        "UPDATE users SET user_level = '2' WHERE tgid = $1;", 
        tgid
    )
    if r is None:
        {"Success": False, "Reason": "User not found"}
    else:
        return {"Success": True, "result": r}
#--------------------------------------------------------------------------

# 8. /admin/
async def admin_level3(tgid: str) -> Dict[str, Any]:
    r = await pg.fetch(
        "UPDATE users SET user_level = '3' WHERE tgid = $1;", 
        tgid
    )
    if r is None:
        {"Success": False, "Reason": "User not found"}
    else:
        return {"Success": True, "result": r}
#--------------------------------------------------------------------------

# 9. /admin/
#async def admin_grep_user(data):
#--------------------------------------------------------------------------

# 10. /admin/
#async def admin_grep_users(data):
# 11. /admin/
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

#|=============================[End Admin panel]=============================|

#|=============================[XUI panel]=============================|

# 1. /xui/
async def xui_login(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Выполняет логин в api XUI и возвращает заголовок аутентификации.

    Args:
        data (Dict[str, Any]): Входные данные, содержащие имя пользователя, пароль и путь полученные при вполнении функции init_server().

    Returns:
        Dict[str, Any]: Заголовок аутентификации 3x-ui или сообщение об ошибке.
    """

    username: str = data.get("username")
    password: str = data.get("passwd")
    web_path: str = data.get("web_path")

    if not all([username, password, web_path]):
        logger.error("Missing required fields in input data: %s", data)
        return {"Success": False, "Reason": "Missing username, password, or web_path"}

    try:
        # Вызов функции для логина
        auth_headers = await xui_func.login(username, password, web_path)
        logger.info("Successfully logged in for user: %s", username)
        return {"Success": True, "auth_headers": auth_headers}
    
    except Exception as ex:
        logger.error("Failed to log in for user %s: %s", username, str(ex))
        return {"Success": False, "Reason": f"Login failed: {ex}"}
#--------------------------------------------------------------------------

# 2. /xui/
async def add_server(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Добавляет сервер в БД

    Args:
        data (Dict[str, Any]): Входные данные, содержащие hostname(ip), порт, имя пользователя и пароль.

    Returns:
        Dict[str, Any]: True в случае успешного выполнения операции либо False и ошибку.
    """

    hostname: str = data.get("hostname")
    port: str = data.get("port")
    username: str = data.get("username")
    passwd: str = data.get("passwd")
    # Проверка на наличие обязательных данных
    if not all([hostname, port, username, passwd]):
        logger.error("Missing required fields in input data: %s", data)
        return {"Success": False, "Reason": "Missing hostname, port, username or passwd"}

    try:
        # Проверка, существует ли сервер с таким hostname в БД
        query_check = "SELECT hostname FROM servers WHERE hostname = $1"
        result_check = await pg.fetch(query_check, hostname)
    
        if result_check:
            logger.error("Server with hostname %s already exists", hostname)
            return {"Success": False, "Reason": "Server already exists in the database"}
        
        # Вставка нового сервера в БД
        query_insert = """
            INSERT INTO servers (hostname, port, username, passwd)
            VALUES ($1, $2, $3, $4)
        """
        values_insert = (hostname, port, username, passwd)
        result_insert = await pg.execute(query_insert, (*values_insert,))

        if result_insert is None:
            logger.info("Server %s successfully inserted into the database", hostname)
            return {"Success": True, "Inserted": result_insert}
        else:
            logger.error("Failed to insert server %s into the database", hostname)
            return {"Success": False, "Reason": "Failed to insert server into the database"}
    except Exception as e:
        # Логирование ошибки с более детализированным сообщением
        logger.exception("Database insertion error for %s: %s", hostname, str(e))
        return {"Success": False, "Reason": f"Failed to insert values into the database: {str(e)}"}
#--------------------------------------------------------------------------

# 3. /xui/
async def init_server(data: Dict[str, Any]) -> Dict[str, Union[bool, str, Any]]:
    """
    Инициализация сервера по предоставленным данным.

    Args:
        data (Dict[str, Any]): Входные данные с информацией о сервере.

    Returns:
        Dict[str, Union[bool, str, Any]]: Результат операции (успех или ошибка).
    """

    hostname: str = data.get("hostname")

    if not hostname:
        logger.error("Hostname is missing from the input data: %s", data)
        return {"Success": False, "Reason": "Missing hostname in input data"}
    
    try:
        # Запрос данных о сервере из БД
        server_info = await pg.fetch(
            "SELECT hostname, port, username, passwd FROM servers WHERE hostname = $1", 
            hostname
        )
        
        if not server_info:
            logger.error("No server found with hostname: %s", hostname)
            return {"Success": False, "Reason": "Server not found in database"}

        # Получение геолокации через geoip
        try:
            geolocation = await xui_func.geo_ip(hostname)
        except Exception as ex:
            logger.warning("Failed to get geolocation for %s: %s. Defaulting to 'RU'.", hostname, str(ex))
            geolocation = "RU"

        # Установка x-ui через импорт файла установщика через scp + ssh
        try:
            ssh_result = await ssh_func.ssh_reg(
                server_info["hostname"], 
                server_info["port"], 
                server_info["username"], 
                server_info["passwd"]
            )
        except Exception as ssh_ex:
            logger.error("SSH registration failed for %s: %s", hostname, str(ssh_ex))
            return {"Success": False, "Reason": f"SSH registration failed: {ssh_ex}"}

        # Обновление данных в БД
        update_query = """
            UPDATE servers 
            SET country = $1, web_user = $2, web_pass = $3, web_path = $4, is_alive = $5
            WHERE hostname = $6
        """

        update_values = (
            geolocation, 
            ssh_result["username"], 
            ssh_result["password"], 
            f"http://{hostname}:2053/{ssh_result['webpath']}", 
            True, 
            hostname
        )
        
        creds_upload = await pg.fetch(update_query, *update_values)

        if creds_upload is None:
            logger.info("Server %s successfully initialized and updated", hostname)
            return {"Success": True, "result": creds_upload}
        else:
            logger.error("Failed to update server credentials for %s", hostname)
            return {"Success": False, "Reason": "Failed to update server credentials"}

    except Exception as ex:
        logger.exception("Unexpected error during server initialization for %s", hostname)
        return {"Success": False, "Reason": f"Unexpected error: {ex}"}
#-------------------------------------------------------------------------- 

# 4. /xui/
async def inbound_creation(data: Dict[str, Any]) -> Dict[str, Union[bool, str, Any]]:
    """
    Создание нового впн клиента и запись его в базу данных.

    Args:
        data (Dict[str, Any]): Входные данные, содержащие информацию о пользователе и хосте.

    Returns:
        Dict[str, Union[bool, str, Any]]: Результат операции (успех или ошибка на все случаи жизни).
    """
    username: str = data.get("web_user")
    password: str = data.get("web_pass")
    web_path: str = data.get("web_path")
    hostname: str = data.get("hostname")

    if not all([username, password, web_path, hostname]):
        logger.error("Missing required fields in data: %s", data)
        return {"Success": False, "Reason": "Missing required fields"}
    
    
    try:
        # Авторизация
        auth_headers = await xui_func.login(username, password, web_path)

        # Создание конфига
        inbound, config, qr_data = await xui_func.add_inbound(auth_headers, web_path, hostname)

        # Запись в БД
        query = """
            INSERT INTO configs (tg_user, inbound, users, config)
            VALUES ($1, $2, $3, $4)
        """

        values = ("test", inbound["remark"], inbound["email"], config)

        result = await pg.fetch(query, *values)
        
        # Проверка результата и перехват ошибок

        if result is None:
            logger.info("Inbound creation successful for %s", inbound["remark"])
            return {"Success": True, "result": config, "qr_data" : qr_data}
        
        logger.error("Insert operation returned None for data: %s", values)
        return {"Success": False, "Reason": "Insert operation failed, returned None"}
    
    except ConnectionError as conn_ex:
        logger.error("Connection error while creating config: %s", str(conn_ex))
        return {"Success": False, "Reason": f"Connection error: {conn_ex}"}
    
    except TimeoutError as timeout_ex:
        logger.warning("Timeout during config creation: %s", str(timeout_ex))
        return {"Success": False, "Reason": f"Timeout occurred: {timeout_ex}"}
    
    except ValueError as val_ex:
        logger.error("Value error during inbound creation: %s", str(val_ex))
        return {"Success": False, "Reason": f"Value error: {val_ex}"}
    
    except Exception as ex:
        logger.exception("Unexpected error during inbound creation")
        return {"Success": False, "Reason": f"Unexpected error: {ex}"}
#--------------------------------------------------------------------------

#|=============================[End XUI panel]=============================|

