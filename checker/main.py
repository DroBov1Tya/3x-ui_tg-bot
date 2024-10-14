import asyncio
import time
from src import api, func
from config import logger

# Главная асинхронная функция
async def main():
    while True:
        await asyncio.sleep(30)

        r = await api.get_servers()
        servers = r.get("result")

        for server in servers:
            hostname = server.get("hostname")
            checker = func.PortChecker(hostname)
            await checker.check_ports()
        invoices = await api.get_invoices()
        await api.process_invoices(invoices)

# Запуск программы
if __name__ == "__main__":
    asyncio.run(main())
