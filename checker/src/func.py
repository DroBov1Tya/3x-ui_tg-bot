import asyncio
from src import api
from config import logger

class PortChecker:
    def __init__(self, hostname):
        self.hostname = hostname

    async def check_port(self, port):
        try:
            reader, writer = await asyncio.open_connection(self.hostname, port)
            writer.close()
            await writer.wait_closed()
            return True
        
        except (asyncio.TimeoutError, ConnectionRefusedError):
            return False
        except OSError as os_ex:
            logger.error(f"OS error while connecting to {self.hostname}:{port} - {str(os_ex)}")
            return False

    async def check_ports(self):
        print(f"Проверяем IP: {self.hostname}")

        # Асинхронная проверка портов
        ssh_task = asyncio.create_task(self.check_port(22))
        port_2053_task = asyncio.create_task(self.check_port(2053))

        ssh_result = await ssh_task
        port_2053_result = await port_2053_task

        # Логирование и действия в зависимости от результата проверки
        await self._process_result(22, ssh_result)
        await self._process_result(2053, port_2053_result)

    async def _process_result(self, port, result):
        if result:
            logger.info("Server %s on port %d is up!", self.hostname, port)
        else:
            logger.info("Server %s on port %d is down!", self.hostname, port)
            # Добавляем лог перед вызовом API-функций
            logger.info("Calling server_down for %s", self.hostname)
            await api.server_down(self.hostname)
            logger.info("Calling remove_configs for %s", self.hostname)
            await api.remove_configs(self.hostname)