import logging
import os
from aiogram import executor

import config
from creation_bot import dp, bot
import handlers
from scheduler import scheduler

logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    scheduler.start()
    await handlers.schedule()
    print("Bot online")


async def on_startup_web(dp):
    await bot.set_webhook(config.URL_APP)
    scheduler.start()
    await handlers.schedule()
    print("Bot online")


async def on_shutdown(dp):
     scheduler.shutdown(wait=False)
     await bot.delete_webhook()


handlers.reg_handlers(dp)

if __name__ == "__main__":
    # executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
    executor.start_webhook(
        dispatcher=dp,
        webhook_path='',
        on_startup=on_startup_web,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
