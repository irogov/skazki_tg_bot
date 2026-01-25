from aiogram import types, Router, Bot
from aiogram.filters import Command
from config.config import load_config

PRICE = types.LabeledPrice(label='Подиска на 1 месяц', amount=29900)
CURRENCY = 'RUB'

config =load_config()

async def buy(message: types.Message):
    if config.pay_set.payments_token.split(':')[1] == 'TEST':
        await message.answer('Тестовый платеж!!!')
    
    await message.answer_invoice(
        title='Подписка на бота на 1 месяц',
        description='Активация подписки',
        provider_token=config.pay_set.payments_token,
        currency=CURRENCY,
        prices=[PRICE],
        start_parameter='one-month-subscription',
        payload=f'sub_30days_{message.from_user.id}'  # ✅ Уникальный payload
    )