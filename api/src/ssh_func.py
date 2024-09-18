import paramiko
import asyncio
import logging
from config import RedisClient

logger = logging.getLogger(__name__)

async def upload_file(ssh_client):
    """
    Загружает локальный файл на удаленный сервер через SFTP.

    Args:
        ssh_client: Активное SSH-соединение для передачи файлов.

    Returns:
        None: Возвращает None в случае успешной загрузки или ошибки.
    """
    local_file_path = "dependencies/installxui.sh"
    remote_file_path = "/root/installxui.sh"

    try:
        sftp = ssh_client.open_sftp()
        
        # Попытка загрузить файл
        sftp.put(local_file_path, remote_file_path)
        logging.info(f"Файл {local_file_path} успешно загружен в {remote_file_path}")

    except FileNotFoundError as fnf_error:
        logging.error(f"Файл не найден: {local_file_path}. Ошибка: {fnf_error}")
    
    except Exception as e:
        logging.error(f"Произошла ошибка при загрузке файла {local_file_path}: {str(e)}")

    finally:
        if sftp:
            sftp.close()
            logging.info("SFTP-соединение закрыто.")

async def xui_init(ssh_client):
    """
    Выполняет скрипт установки xui на удаленном сервере через SSH.

    Args:
        ssh_client: Активное SSH-соединение для выполнения команд.

    Returns:
        None: Возвращает None в случае ошибки или завершения скрипта.
    """
    try:
        # Выполнение bash-скрипта для установки xui
        stdin, stdout, stderr = ssh_client.exec_command('bash /root/installxui.sh')
        stdout.channel.recv_exit_status()

        # Чтение ошибок, если они есть
        error_output = stderr.read().decode('utf-8').strip()
        if error_output:
            logging.error(f"Ошибка при выполнении скрипта установки xui: {error_output}")
            return

        logging.info("Скрипт установки xui выполнен успешно.")

    except Exception as e:
        logging.error(f"Произошла ошибка при выполнении скрипта установки xui: {str(e)}")

async def get_cred(ssh_client) -> dict:
    """
    Получает учетные данные с удаленного сервера через SSH.

    Args:
        ssh_client: Активное SSH-соединение.

    Returns:
        dict: Словарь с учетными данными (username, password, webpath) или None в случае ошибки.
    """
    try:
        # Выполнение команды для чтения файла
        stdin, stdout, stderr = ssh_client.exec_command('cat /root/cred.txt')
        stdout.channel.recv_exit_status()

        # Чтение вывода команды
        creds_output = stdout.read().decode('utf-8').strip().split()

        # Чтение ошибок команды
        error_output = stderr.read().decode('utf-8').strip()
        if error_output:
            logging.error(f"Ошибка при чтении файла cred.txt: {error_output}")
            return None

        # Проверка на достаточное количество данных
        if len(creds_output) != 3:
            logging.error(f"Недостаточно данных в файле cred.txt: {creds_output}")
            return None

        # Формирование результата
        result = {
            "username": creds_output[0],
            "password": creds_output[1],
            "webpath": creds_output[2]
        }
        
        logging.info(f"Credentials successfully retrieved: {result}")
        return result

    except Exception as e:
        logging.error(f"Ошибка при получении учетных данных: {str(e)}")
        return None

async def ssh_reg(hostname: str, port: int, username: str, passwd: str) -> dict:
    """
    Устанавливает SSH-соединение, загружает файл и устанавливаем VPN сервер.

    Args:
        hostname (str): Хост для подключения по SSH.
        port (int): Порт для подключения по SSH.
        username (str): Имя пользователя для SSH.
        passwd (str): Пароль для SSH.

    Returns:
        dict: Учетные данные веб сервера.
    """
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Устанавливаем SSH-соединение
        ssh_client.connect(hostname=hostname, port=port, username=username, password=passwd)
        logging.info(f"SSH connection to {hostname} established.")

        # Загружаем файл на сервер
        await upload_file(ssh_client)
        logging.info(f"File uploaded to {hostname}.")

        # Инициализация XUI
        await xui_init(ssh_client)
        logging.info(f"XUI initialization on {hostname} completed.")

        # Получаем учетные данные
        creds = await get_cred(ssh_client)
        logging.info(f"Credentials retrieved from {hostname}.")
    
    except paramiko.SSHException as e:
        logging.error(f"SSH connection failed: {str(e)}")
        return {"Success": False, "Reason": f"SSH connection failed: {str(e)}"}
    
    except Exception as e:
        logging.error(f"Error during SSH operations: {str(e)}")
        return {"Success": False, "Reason": f"Error during SSH operations: {str(e)}"}

    finally:
        # Закрываем SSH-соединение
        ssh_client.close()
        logging.info(f"SSH connection to {hostname} closed.")

    return creds

if __name__ == "__main__":
    asyncio.run(ssh_reg())