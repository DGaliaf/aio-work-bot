import asyncio
import logging
import uuid

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from config import Config, get_config

from src.handlers import routers

logger = logging.getLogger(__name__)


async def main():
    # TODO: Bypass

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    config: Config = get_config()

    print(config)

    bot: Bot = Bot(token=config.bot_token, default=DefaultBotProperties(parse_mode='HTML'))
    dp: Dispatcher = Dispatcher()

    for router in routers:
        dp.include_router(router)

    logger.info("Starting bot")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
