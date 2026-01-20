from services.fairytale import get_story, prepare_book, normalize_text
from aiogram import Bot
from config.config import Config
import random, asyncio
from assets.other import send_fairy_picture


async def send_daily_story(bot: Bot, config: Config, client):
    random_group = random.choice([1, 2, 3])
    to_sleep = 1
    tale, group = await get_story(random_group, client)
    tale_normalized = normalize_text(tale)
    tales = prepare_book(tale_normalized)
    channel = config.channel_id
    link_to_bot = 'Нужно больше сказок и баек? Подпишись на наш бот ' \
    '<a href="https://t.me/skazki_i_baiki_bot">Сказки и байки Бот</a>.'
    try:
        await send_fairy_picture(channel, bot=bot)
        await asyncio.sleep(to_sleep)
    except Exception as e:
        print(e)
        
    for text in tales.values():
        try:
            await bot.send_message(chat_id=channel, text=text)
            await asyncio.sleep(to_sleep)
        except Exception as e:
            return False
        
    try:
        await bot.send_message(chat_id=channel, text=link_to_bot, parse_mode='HTML')
        await asyncio.sleep(to_sleep)
    except Exception as e:
        return False
    return True

# async def db_daily_population(client):
#     for gr in range(1,4):
#         for _ in range(30):
#             tale_text, group = await get_story(gr, client)
#             await add_tale(tale_text=tale_text, tale_group=group, rating=5)


