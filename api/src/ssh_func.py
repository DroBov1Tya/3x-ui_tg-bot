import paramiko
import asyncio


async def upload_file(ssh_client):
    sftp = ssh_client.open_sftp()
    local_file_path = "dependencies/installxui.sh"
    remote_file_path = "/root/installxui.sh"
    try:
        sftp.put(local_file_path, remote_file_path)
        print(f"Файл {local_file_path} успешно загружен в {remote_file_path}")
        sftp.close()
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

async def xui_init(ssh_client):
    try:
        stdin, stdout, stderr = ssh_client.exec_command('bash /root/installxui.sh')
        stdout.channel.recv_exit_status()

        error_output = stderr.read().decode('utf-8')
        if error_output:
            print(f"Ошибка при выполнении скрипта: {error_output}")
            return
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

async def get_cred(ssh_client):
    try:
        stdin, stdout, stderr = ssh_client.exec_command('cat /root/cred.txt')
        stdout.channel.recv_exit_status()
        creds_output = stdout.read().decode('utf-8')
        creds_output = creds_output.split()

        error_output = stderr.read().decode('utf-8')
        if error_output:
            print(f"Ошибка при чтении файла: {error_output}")
            return None
        
        if len(creds_output) < 3:
            print(f"Недостаточно данных в файле cred.txt: {creds_output}")
            return None
        
        result = {
            "username" : creds_output[0],
            "password" : creds_output[1],
            "webpath" : creds_output[2]
        }
        return result
        
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

async def ssh(port, user, host, passwd):
    PORT = port
    USERNAME = user
    HOSTNAME = host
    PASSWORD = passwd

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=HOSTNAME,port=PORT,username=USERNAME,password=PASSWORD)

    await upload_file(ssh_client)
    await xui_init(ssh_client)
    creds = await get_cred(ssh_client)
    ssh_client.close()
    return creds

if __name__ == "__main__":
    asyncio.run(ssh())