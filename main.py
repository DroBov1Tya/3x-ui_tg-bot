import asyncio
import modules


async def main(username, password):

    auth_headers = await modules.login(username, password)
    await modules.add_inbound(auth_headers)


if __name__ == "__main__":
    username, password = 'd2nNd1Ha', 'omCOLPrE'
    asyncio.run(main(username, password)) 
