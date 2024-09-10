import asyncio
import modules.xui_logic as xui_logic


async def main(username, password):
    auth_headers = await xui_logic.login(username, password)

    await xui_logic.add_inbound(auth_headers)
    # await logic.get_list(auth_headers)
    # await logic.delete_inbound(auth_headers, inbound)
    # await logic.add_client(auth_headers)


if __name__ == "__main__":
    username, password = 'O7ndSNCL', '/HaciQVw'
    asyncio.run(main(username, password)) 
