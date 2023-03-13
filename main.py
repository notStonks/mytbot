import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
from creation_bot import dp
import handlers
# from database import db

logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    asyncio.create_task(handlers.scheduler())
    print("Bot online")



handlers.reg_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)





