import asyncio
import logging
import uuid

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from config import Config, load_config
from config.base import getenv
from src.handlers import echo


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")

    config: Config = load_config()

    if str(uuid.getnode()) in getenv("ALLOWED_MACS"):
        bot: Bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode='HTML'))
        dp: Dispatcher = Dispatcher()

        dp.include_router(echo.router)

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    else:
        logger.info("User not allowed to start the bot")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
