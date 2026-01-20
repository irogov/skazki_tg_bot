from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from database.crud import add_user, fetch_tale, add_tale_to_tales_for_users
from lexicon.lexicon import LEXICON_RU
from keyboards.kb import age_keyboard
from services.fairytale import prepare_book, normalize_text
import asyncio

from assets.other import answer_photo
import random

user_router = Router()

async def process_group_n_tale(message: Message, group, conn):
    to_sleep = 1
    user_tel_id = message.from_user.id
    tale_id, tale_text = await fetch_tale(conn=conn, user_tel_id=user_tel_id, group=group)
    await add_tale_to_tales_for_users(conn=conn, user_tel_id=user_tel_id, tale_id=tale_id)
    tale_text_normalized = normalize_text(tale_text)
    tale_list = prepare_book(tale_text_normalized)
    await answer_photo(message=message)
    await asyncio.sleep(to_sleep)
    for page in tale_list.values():
        await message.answer(page)
        await asyncio.sleep(to_sleep)

@user_router.message(CommandStart())
async def process_start_command(message: Message, **kwargs):
    conn = kwargs.get('conn')
    user_tel_id = message.from_user.id
    await add_user(conn=conn, user_tel_id=user_tel_id)
    await message.answer(LEXICON_RU['/start'], reply_markup=age_keyboard)

@user_router.message(F.text == LEXICON_RU['1'])
async def return_group_one_tale(message: Message, **kwargs):
    conn = kwargs.get('conn')
    await process_group_n_tale(message, 1, conn)

@user_router.message(F.text == LEXICON_RU['2'])
async def return_group_one_tale(message: Message, **kwargs):
    conn = kwargs.get('conn')
    await process_group_n_tale(message, 2, conn)

@user_router.message(F.text == LEXICON_RU['3'])
async def return_group_one_tale(message: Message, **kwargs):
    conn = kwargs.get('conn')
    await process_group_n_tale(message, 3, conn)

@user_router.message(F.text=='/help')
async def process_help_command(message: Message):
    await message.answer(LEXICON_RU['/help'], reply_markup=age_keyboard)

@user_router.message()
async def process_other_messages(message: Message):
    await message.answer(LEXICON_RU['other'])

    
