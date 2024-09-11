import asyncio
from api.src import xui_func


async def main(username, password, path):
    auth_headers = await xui_func.login(username, password, path)

    await xui_func.add_inbound(auth_headers)
    # await logic.get_list(auth_headers)
    # await logic.delete_inbound(auth_headers, inbound)
    # await logic.add_client(auth_headers)


if __name__ == "__main__":
    username, password = 'C1wMa9ud', 'MiA/YxqU'
    path = "http://191.96.235.118:2053/YV6m0FM4NE"
    asyncio.run(main(username, password)) 
