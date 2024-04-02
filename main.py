import asyncio
import contextlib
import logging
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F

from handlers.user import user_router
from handlers.admin import admin_router

from middleware.db import DataBaseSession


load_dotenv()

from database.engine import create_db, session_maker

bot = Bot(os.getenv("BOT_TOKEN"))  # make .env file with bot token
dp = Dispatcher()
dp.include_router(user_router)
dp.include_router(admin_router)
logger = logging.getLogger(__name__)

ALLOWED_UPDATES = ['message, edited_message']


async def on_startup(bot):
    await create_db()


async def on_shutdown(bot):
    print('бот лег')


async def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s")
    logger.info("Starting bot...")
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(main())
