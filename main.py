import database
import asyncio


async def main():
    await database.init_models()


asyncio.run(main())




