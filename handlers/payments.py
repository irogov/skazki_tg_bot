from aiogram import types, Router, Bot, F
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU

payment_router = Router()

@payment_router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery, bot: Bot):
    print(f"💳 Pre-checkout: {pre_checkout_q.total_amount} {pre_checkout_q.currency}")
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@payment_router.message(F.successful_payment)
async def successful_payment(message: types.Message, db_pool):
    print('Успешная оплата!!!')

@payment_router.message()
async def process_other_messages(message: Message):
    await message.answer(LEXICON_RU['other'])