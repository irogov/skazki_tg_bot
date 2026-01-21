import logging
from openai import AsyncOpenAI
from aiogram import Bot, Dispatcher
from database.connection import get_pg_pool
import psycopg_pool
from handlers.user import user_router
from config.config import Config, load_config
from middleware.database_mw import DataBaseMiddleware
from services.daily_routines import send_daily_story
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.crud import db_daily_population

logger = logging.getLogger(__name__)

async def main(config: Config, bot: Bot):
    logger.info('Starting bot...')
    
    dp = Dispatcher()

    db_pool: psycopg_pool.AsyncConnectionPool = await get_pg_pool(
        db_name=config.db.name,
        host=config.db.host,
        port=config.db.port,
        user=config.db.user,
        password=config.db.password
    )
    config = load_config()
    deepseek_key = config.ai
    client = AsyncOpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com")

    logger.info('Getting routers')
    dp.include_routers(user_router)

    # Подключаем миддлвари в нужном порядке
    logger.info("Including middlewares...")
    dp.update.middleware(DataBaseMiddleware())

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_daily_story,
        # 'interval',
        # minutes=5,
        'cron',
        hour=19,
        args=[bot, config, client],  # Передаем экземпляр бота в функцию
        timezone="Europe/Moscow",
    )

    scheduler.add_job(
        db_daily_population,
        'cron',
        hour=2,
        minute=15,
        args=[db_pool, client],
        timezone="Europe/Moscow",
        id="daily_fairytales",
        replace_existing=True,
        misfire_grace_time=600  # 10 мин на генерацию 50 сказок
    )

    scheduler.start()

    try:
        await dp.start_polling(
            bot, 
            db_pool=db_pool
        )
    except Exception as e:
        logger.exception(e)
    finally:
        await db_pool.close()
        logger.info("Connection to Postgres closed")
