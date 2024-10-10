import logging
import time
from config import PostgreSQL
from src import redis_func
from src import xui_func
from src import ssh_func
from src.generator_func import voucher_generator
from typing import Dict, Any, Union

pg = PostgreSQL()
logger = logging.getLogger(__name__)

async def handle_exception(ex: Exception) -> Dict[str, Any]:
    if isinstance(ex, ConnectionError):
        logger.error("Connection error: %s", str(ex))
        return {"Success": False, "Reason": f"Connection error: {ex}"}
    
    elif isinstance(ex, TimeoutError):
        logger.warning("Timeout occurred: %s", str(ex))
        return {"Success": False, "Reason": f"Timeout occurred: {ex}"}
    
    elif isinstance(ex, ValueError):
        logger.error("Value error: %s", str(ex))
        return {"Success": False, "Reason": f"Value error: {ex}"}
    
    else:
        logger.exception("Unexpected error occurred")
        return {"Success": False, "Reason": f"Unexpected error: {ex}"}



#|=============================[User panel]=============================|
# 1. /user/create
async def sync_sequence():
    """
    """

    query = '''
    SELECT setval(
        'users_id_seq', 
        (SELECT COALESCE(MAX(id), 1) FROM users)
    );
    '''

    try:
        await pg.execute(query)
    except Exception as ex:
        return await handle_exception(ex)

async def user_create(data: Dict[str, Any]) -> Dict[str, Any]:
    # Синхронизируем последовательность перед вставкой новых данных
    await sync_sequence()

    userinfo = data['user']
    tgid = userinfo['tgid']
    nickname = userinfo['nickname']
    first_name = userinfo['first_name']
    last_name = userinfo['last_name']
    
    query = """
        INSERT INTO users 
        (tgid, nickname, first_name, last_name, is_banned) 
        VALUES ($1, $2, $3, $4, $5) 
        ON CONFLICT (tgid) DO NOTHING RETURNING true;
    """
    values = (tgid, nickname, first_name, last_name, True)
    
    try:
        r = await pg.fetch(query, *values)
        if r is None:
            return {"Success": False, "Reason": "User already exists"}
        else:
            return {"Success": True}
        
    except Exception as ex:
        return await handle_exception(ex)
#--------------------------------------------------------------------------

# 2. /user/{tgid}
async def user_info(tgid: str) -> Dict[str, Any]:
    """
    """

    query = '''
        SELECT * FROM users WHERE tgid = $1;
    '''
    
    try:
        r = await pg.fetch(query, tgid)

        if r is None:
            return {"Success": False, "Reason": "User not found"}
        else:
            return {"Success": True, "user": r }
        
    except Exception as ex:
        return await handle_exception(ex)
#--------------------------------------------------------------------------

# 3. /user/agree/{tgid}
async def agree(tgid: str) -> Dict[str, Any]:
    """
    """

    query = '''
        UPDATE users
        SET is_banned = False
        WHERE tgid = $1;
    '''
    
    try:
        r = await pg.fetch(query, tgid)

        if r is None:
            return {"Success": False, "Reason": "User not found"}
        else:
            return {"Success": True, "user": r }
        
    except Exception as ex:
        return await handle_exception(ex)
#--------------------------------------------------------------------------

# 4. /user/checkvoucher
async def checkvoucher(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Функция для проверки ваучера в базе данных. 
    Возвращает информацию о ваучере: его статус (активен или нет), длительность и срок действия.

    Args:
        data (Dict[str, Any]): Словарь, содержащий код ваучера.

    Returns:
        Dict[str, Any]: Результат проверки ваучера (успех, ошибки, статус ваучера).
    """

    voucher_code = data.get("voucher_code")

    if not voucher_code:
        return {"Success": False, "Reason": "Voucher code is missing."}

    query_voucher = '''
    SELECT duration, is_used, expires_at FROM vouchers WHERE code = $1;
    '''
    
    try:
        voucher = await pg.fetch(query_voucher, voucher_code)

        if not voucher:
            return {"Success": False, "Reason": "Voucher not found."}

        if voucher["is_used"]:
            return {"Success": False, "Reason": "Voucher has already been used."}

        current_time = int(time.time())
        if voucher["expires_at"] < current_time:
            return {"Success": False, "Reason": "Voucher has expired."}

        return {
            "Success": True
        }
    
    except Exception as ex:
        return await handle_exception(ex)
#--------------------------------------------------------------------------

# 5. /user/activatevoucher
async def activate_voucher(data: Dict[str, Any]) -> Dict[str, Any]:
    '''
    Функция активации ваучера и обновления срока подписки пользователя.

    Args:
        data (dict): Словарь, содержащий "tgid" (ID пользователя) и "voucher_code" (код ваучера).

    Returns:
        dict: Результат активации (успех или ошибка).
    '''

    tgid = int(data.get("tgid"))
    voucher_code = str(data.get("voucher_code"))
    old_voucher = int(data.get("subscription"))
    lang = str(data.get("lang"))

    if not tgid or not voucher_code:
        logging.error("TGID or voucher code is missing.")
        if lang == "en":
            return {"Success": False, "Reason": "TGID or voucher code is missing."}
        elif lang == "ru":
            return {"Success": False, "Reason": "TGID или код ваучера отсутствует."}


    query_voucher = '''
    SELECT duration, is_used, expires_at FROM vouchers WHERE code = $1;
    '''
    try:
        voucher = await pg.fetch(query_voucher, voucher_code)

        if not voucher:
            logging.error(f"Voucher with code {voucher_code} not found.")
        if lang == "en":
            return {"Success": False, "Reason": "Voucher not found."}
        elif lang == "ru":
            return {"Success": False, "Reason": "Ваучер не найден."}
    
        if voucher["is_used"]:
            logging.error(f"Voucher {voucher_code} has already been used.")
            if lang == "en":
                return {"Success": False, "Reason": "Voucher has already been used."}
            elif lang == "ru":
                return {"Success": False, "Reason": "Ваучер уже был использован."}

        current_time = int(time.time())
        if voucher["expires_at"] < current_time:
            logging.error(f"Voucher {voucher_code} has expired.")
            if lang == "en":
                return {"Success": False, "Reason": "Voucher has expired."}
            elif lang == "ru":
                return {"Success": False, "Reason": "Срок действия ваучера истек."}


        voucher_duration = int(voucher["duration"])
        new_sub_expiration = max(current_time, old_voucher) + voucher_duration
        logging.info(f"New subscription expiration for TGID {tgid}: {new_sub_expiration} (Unix time)")

        query_update_sub = '''
        UPDATE users 
        SET sub = $1 
        WHERE tgid = $2
        RETURNING id;
        '''
        result_sub = await pg.fetch(query_update_sub, new_sub_expiration, tgid)

        if result_sub is None:
            logging.error(f"Failed to update subscription for TGID: {tgid}")
            if lang == "en":
                return {"Success": False, "Reason": "Failed to update subscription."}
            elif lang == "ru":
                return {"Success": False, "Reason": "Не удалось обновить подписку."}

        logging.info(f"Subscription for TGID {tgid} updated successfully with ID: {result_sub['id']}")

        query_update_voucher = '''
        UPDATE vouchers 
        SET is_used = true 
        WHERE code = $1 
        RETURNING id;
        '''
        result_voucher = await pg.fetch(query_update_voucher, voucher_code)

        if result_voucher is None:
            logging.error(f"Failed to mark voucher {voucher_code} as used.")
            if lang == "en":
                return {"Success": False, "Reason": "Failed to mark voucher as used."}
            elif lang == "ru":
                return {"Success": False, "Reason": "Не удалось отметить ваучер как использованный."}

        logging.info(f"Voucher {voucher_code} marked as used with ID: {result_voucher['id']}")

        if lang == "en":
            return {"Success": True, "New Sub Expiration": new_sub_expiration}
        elif lang == "ru":
            return {"Success": True, "Новое время окончания подписки": new_sub_expiration}
    
    except Exception as ex:
        logging.error(f"Error during voucher activation: {str(ex)}")
        if lang == "en":
            return {"Success": False, "Reason": "Internal server error."}
        elif lang == "ru":
            return {"Success": False, "Reason": "Внутренняя ошибка сервера."}
#--------------------------------------------------------------------------

# 6. /user/getsubscription/{tgid}
async def getsubscription(tgid: int) -> Dict[str, Any]:
    """
    Получение времени подписки по идентификатору Telegram пользователя.
    """
    if not tgid:
        logging.error("TGID is missing.")
        return {"Success": False, "Reason": "TGID is missing."}
    
    query = '''
        SELECT sub
        FROM users
        WHERE tgid = $1;
    '''

    try:
        r = await pg.fetch(query, tgid)  
        if not r:
            return {"Success": False, "Reason": "Can't find subscription"}
        else:
            subscription = r['sub']
            return {"Success": True, "subscription": subscription}
        
    except Exception as ex:
        return await handle_exception(ex)
#--------------------------------------------------------------------------

# 7. /user/setlanguage
async def setlanguage(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Изменение языка бота для пользователя на Русский
    """

    lang = data.get("lang")
    tgid = data.get("tgid")

    if not tgid:
        logging.error("TGID is missing.")
        return {"Success": False, "Reason": "TGID is missing."}
    if not lang:
        logging.error("Language is missing.")
        return {"Success": False, "Reason": "Language is missing."}
    
    query = '''
        UPDATE users
        SET lang = $1
        WHERE tgid = $2;
    '''

    values = (lang, tgid)
    try:
        r = await pg.execute(query, values)  
        if not r:
            return {"Success": False, "Reason": "Can't update language"}
        else:
            return {"Success": True}
        
    except Exception as ex:
        return await handle_exception(ex)
#--------------------------------------------------------------------------

# 8. /user/checklanguage/{tgid}
async def checklanguage(tgid: int) -> Dict[str, Any]:
    """
    """

    if not tgid:
        logging.error("TGID is missing.")
        return {"Success": False, "Reason": "TGID is missing."}
    
    query = '''
        SELECT lang
        FROM users
        WHERE tgid = $1;
    '''

    try:
        r = await pg.fetch(query, tgid)  
        if not r:
            return {"Success": False, "Reason": "Can't find language"}
        else:
            lang = r['lang']
            return {"Success": True, "lang": lang}
        
    except Exception as ex:
        return await handle_exception(ex)
#--------------------------------------------------------------------------

# 9. /user/configlimit/{tgid}
async def configlimit(tgid: int) -> Dict[str, Any]:
    """
    """

    if not tgid:
        logging.error("TGID is missing.")
        return {"Success": False, "Reason": "TGID is missing."}
    
    query = '''
        SELECT configlimit
        FROM users
        WHERE tgid = $1;
    '''

    try:
        r = await pg.fetch(query, tgid)  
        if not r:
            return {"Success": False, "Reason": "Can't find configlimit"}
        else:
            configlimit = r['configlimit']
            return {"Success": True, "configlimit": configlimit}
        
    except Exception as ex:
        return await handle_exception(ex)
#--------------------------------------------------------------------------
#|=============================[End User panel]=============================|

#|=============================[Admin panel]=============================|
# 1. /admin/isadmin/{tgid}
async def is_admin(tgid: str) -> Dict[str, Any]:
    query = """
        SELECT is_admin FROM users WHERE tgid = $1;
    """
    try:
        r = await pg.fetch(query, tgid)

        if r['is_admin'] is False:
            return {"Success": False, "Reason": "User not admin"}
        else:
            return {"Success": True}
    except Exception as ex:
        return await handle_exception(ex)
#--------------------------------------------------------------------------

# 2. /admin/ban/{tgid}
async def admin_ban(tgid: str) -> Dict[str, Any]:

    query = """
    UPDATE users
    SET is_banned = TRUE
    WHERE tgid = $1;
    """

    try:
        r = await pg.fetch(query, tgid)
        if r is None:
            {"Success": False, "Reason": "User not found"}
        else:
            return {"Success": True, "result": r}
        
    except Exception as ex:
        return await handle_exception(ex)
#--------------------------------------------------------------------------

# 3. /admin/unban/{tgid}
async def admin_unban(tgid: str) -> Dict[str, Any]:
    """
    """

    query = '''
    UPDATE users
    SET is_banned = FALSE
    WHERE tgid = $1;
    '''

    try:
        r = await pg.fetch(query, tgid)
        if r is None:
            {"Success": False, "Reason": "User not found"}
        else:
            return {"Success": True, "result": r}
        
    except Exception as ex:
        return await handle_exception(ex)
#--------------------------------------------------------------------------

# 4. /admin/fetchadmins
async def admin_fetchadmins() -> Dict[str, Any]:
    """
    """

    query = '''
    SELECT tgid 
    FROM users 
    WHERE is_admin = True;
    '''

    try:
        r = await pg.fetchall(query)
        if r is None:
            {"Success": False, "Reason": "No found admins"}
        else:
            ids = []
            for admin in r:
                ids.append(admin['tgid'])
            return {"Success": True, "result": ids}
        
    except Exception as ex:
        return await handle_exception(ex)
#--------------------------------------------------------------------------

# 5. /admin/voucherone
async def admin_create_voucher_one():
    """
    Функция для создания ваучера на 1 месяц подписки.
    Длительность ваучера указана в секундах (30 дней = 2592000 секунд).
    """
    voucher_code = await voucher_generator()

    # Длительность подписки (30 дней в секундах)
    duration = 2592000  # 30 дней * 24 часа * 60 минут * 60 секунд

    # Текущее время в Unix формате
    current_time = int(time.time())

    # Дата истечения действия ваучера через 6 месяцев в Unix-время
    expires_at = current_time + duration  # Текущее время + 30 дней

    query = '''
    INSERT INTO vouchers (code, discount_type, duration, is_used, created_at, expires_at)
    VALUES ($1, 'subscription', $2, false, $3, $4)
    RETURNING id;
    '''
    
    try:
        result = await pg.execute(query, (voucher_code, duration, current_time, expires_at))
        return {"Success": True, "result": result, "voucher": voucher_code}
    
    except Exception as ex:
        return await handle_exception(ex)
#--------------------------------------------------------------------------

# 6. /admin/vouchersix
async def admin_create_voucher_six():
    """
    Функция для создания ваучера на 6 месяцев подписки.
    Длительность ваучера указана в секундах (6 месяцев = 15552000 секунд).
    """

    voucher_code = await voucher_generator()

    duration = 15552000 

    current_time = int(time.time())

    expires_at = current_time + duration

    query = '''
    INSERT INTO vouchers (code, discount_type, duration, is_used, created_at, expires_at)
    VALUES ($1, 'subscription', $2, false, $3, $4)
    RETURNING id;
    '''
    
    try:
        result = await pg.execute(query, (voucher_code, duration, current_time, expires_at))
        return {"Success": True, "result": result, "voucher": voucher_code}
    
    except Exception as ex:
        return await handle_exception(ex)
#--------------------------------------------------------------------------

# 7. /admin/voucheryear
async def admin_create_voucher_year():
    """
    Функция для создания ваучера на 1 год подписки.
    Длительность ваучера указана в секундах (1 год = 31536000 секунд).
    """
    voucher_code = await voucher_generator()

    # Длительность подписки (365 дней в секундах)
    duration = 31536000  # 365 дней * 24 часа * 60 минут * 60 секунд

    # Текущее время в Unix формате
    current_time = int(time.time())

    # Дата истечения действия ваучера через 1 год в Unix-время
    expires_at = current_time + duration  # Текущее время + 365 дней

    query = '''
    INSERT INTO vouchers (code, discount_type, duration, is_used, created_at, expires_at)
    VALUES ($1, 'subscription', $2, false, $3, $4)
    RETURNING id;
    '''
    
    try:
        result = await pg.execute(query, (voucher_code, duration, current_time, expires_at))
        return {"Success": True, "result": result, "voucher": voucher_code}
    
    except Exception as ex:
        return await handle_exception(ex)
#--------------------------------------------------------------------------

#|=============================[XUI panel]=============================|
# 1. /xui/init_server
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
        return await handle_exception(ex)
#--------------------------------------------------------------------------

# 2. /xui/xui_login
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
        return await handle_exception(ex)
#--------------------------------------------------------------------------

# 3. /xui/inbound_creation
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
    tgid:     int = data.get("tgid")
    tg_user:   str = data.get("tg_nick")

    if not all([username, password, web_path, hostname, tgid, tg_user]):
        logger.error("Missing required fields in data: %s", data)
        return {"Success": False, "Reason": "Missing required fields"}
    
    
    try:
        # Шаг 1: Получаем значение подписки из БД
        query_sub = """
            SELECT sub FROM users WHERE tgid = $1;
        """
        user_sub = await pg.fetch(query_sub, tgid)

        if user_sub['sub'] is None:
            logger.error("User subscription is not active or tgid %s not found ", tgid)
            return {"Success": False, "Reason": "Your subscription is not active."}
        
        current_time = int(time.time())  # Текущее время в формате Unix
        if int(user_sub['sub']) < int(current_time):
            return {"Success": False, "Reason": "Your subscription is not active."}

        # Авторизация
        auth_headers = await xui_func.login(username, password, web_path)

        # Создание конфига
        inbound, config, qr_data = await xui_func.add_inbound(auth_headers, web_path, hostname)

        # Запись в БД
        query = """
            INSERT INTO configs (hostname, tg_user, inbound, users, config)
            VALUES ($1, $2, $3, $4, $5);
        """

        query_history = """
            INSERT INTO configs_history (hostname, tg_user, inbound, users, config)
            VALUES ($1, $2, $3, $4, $5);
        """

        values = (hostname, tg_user, inbound["remark"], inbound["email"], config)

        result = await pg.execute(query, values)
        # Проверка результата и перехват ошибок

        if result is None:
            logger.info("Inbound creation successful for %s", inbound["remark"])
            await pg.execute(query_history, values)
            return {"Success": True, "result": result, "config": config, "qr_data": qr_data, "inbound" : inbound}
        
        logger.error("Insert operation returned None for data: %s", values)
        return {"Success": False, "Reason": "Insert operation failed, returned None"}
    
    except Exception as ex:
        return await handle_exception(ex)
#--------------------------------------------------------------------------

# 4. /xui/servers_count
async def servers_count() -> Dict[str, Union[bool, str, Any]] :
    """
    Забирает из БД информацию о активных серверов для динамического вывода кнопок в бота

    Args:
        -

    Returns:
        Dict[str, Union[bool, str, Any]]: Результат операции (успех или ошибка).
    """

    query = '''
        SELECT * FROM servers
        WHERE is_alive = true;
    '''
    try:
        result = await pg.fetchall(query)
        if result:
            logger.info("Select successful for %s", query)
            return {"Success": True, "result" : result}
        else:
            return None
        
    except Exception as ex:
        return await handle_exception(ex)
#--------------------------------------------------------------------------

# 5. /xui/server_info/{hostname}
async def server_info(hostname) -> Dict[str, Union[bool, str, Any]] :
    """
    Забирает из БД информацию о одном конкретном сервере

    Args:
        -

    Returns:
        Dict[str, Union[bool, str, Any]]: Результат операции (успех или ошибка).
    """

    query = '''
        SELECT * FROM servers
        WHERE hostname = $1;
    '''
    try:
        result = await pg.fetch(query, hostname)
        if result:
            logger.info("Select successful for %s", query)
            return {"Success": True, "result" : result}
        
    except Exception as ex:
        return await handle_exception(ex)
#--------------------------------------------------------------------------

# 6. /xui/remove_configs/{hostname}
async def remove_configs(hostname: str) -> Dict[str, Union[bool, str, Any]]:
    """
    Удаление конфигураций по hostname.
    """
    query = '''
        DELETE FROM configs
        WHERE hostname = $1;
    '''
    try:
        logger.info(f"Удаляем конфигурации для хоста: {hostname}")
        r = await pg.execute(query, (hostname,))
        logger.info(f"Результат удаления: {r}")
        if r == 'DELETE 0':
            return {"Success": False, "Reason": "No records found to delete"}
        else:
            return {"Success": True, "result": r}

    
    except Exception as ex:
        logger.error(f"Ошибка при удалении конфигураций для хоста {hostname}: {str(ex)}")
        return await handle_exception(ex)


#|===============================[Servers panel]===============================|
# 1. /servers/add_server
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
        
    except Exception as ex:
        return await handle_exception(ex)
#--------------------------------------------------------------------------

# 2. /servers/get_servers
async def get_servers() -> Dict[str, Any]:
    query = '''
        SELECT * FROM servers WHERE is_alive is TRUE;
    '''
    try:
        r = await pg.fetchall(query)
        return {"Success" : True, "result" : r}
    
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

# 3. /servers/server_down
async def server_down(data: Dict[str, Any]) -> Dict[str, Any]:
    host: str = data.get("hostname")
    query = '''
        UPDATE servers SET is_alive = FALSE WHERE hostname = $1
    '''

    try:
        # Добавляем await для выполнения запроса к базе данных
        r = await pg.fetch(query, host)
        return {"Success": True, "result": r}
    
    except Exception as ex:
        return await handle_exception(ex)
