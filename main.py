import asyncio
import logging
from app.bot import main
from aiogram import Bot, Dispatcher
from config.config import load_config, Config
from handlers.user import user_router
# from handlers.other import other_router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

logger = logging.getLogger(__name__)

config = load_config()
bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

asyncio.run(main(config, bot))
