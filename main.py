import asyncio
import modules


async def main(username, password):
    # inbound = str("3")
    auth_headers = await modules.login(username, password)
    await modules.add_inbound(auth_headers)
    # await modules.get_list(auth_headers)
    # await modules.delete_inbound(auth_headers, inbound)
    # await modules.add_client(auth_headers)


if __name__ == "__main__":
    username, password = '/DNNyaay', 'bId5A/Ho'
    asyncio.run(main(username, password)) 
