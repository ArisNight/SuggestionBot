import asyncio
import atexit
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from signal import signal, SIGINT, SIGTERM

from app.handlers import router
from app.database import db
from app.logger import logger
from config import BOT_TOKEN

async def shutdown(dp: Dispatcher):
    logger.info("Shutting down...")
    await dp.storage.close()
    await dp.storage.wait_closed()
    db.close()

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)

    try:
        logger.info("Starting bot...")
        await dp.start_polling(bot)
    finally:
        await shutdown(dp)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by keyboard interrupt")
    except Exception as e:
        logger.error(f"Critical error: {e}")
    finally:
        loop.close()
        logger.info("Bot stopped")