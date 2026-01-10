from aiogram.types import FSInputFile
from pathlib import Path
import random
from aiogram.types import Message

HERE = Path(__file__).resolve().parent

async def send_fairy_picture(chat_id, bot):
    i = random.choice([1,2,3])
    pic_path = HERE / f'{i}.png'
    pic = FSInputFile(pic_path)
    await bot.send_photo(chat_id, pic)

async def answer_photo(message: Message):
    i = random.choice([1,2,3])
    print(i)
    pic_path = HERE / f'{i}.png'
    pic = FSInputFile(pic_path)
    await message.answer_photo(pic)