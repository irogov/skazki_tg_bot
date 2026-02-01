from aiogram import types, Router, Bot
from aiogram.filters import Command
from config.config import load_config
import json

price_rub = 299
PRICE = types.LabeledPrice(label='Подиска на 1 месяц', amount=price_rub * 100)
CURRENCY = 'RUB'

config =load_config()

provider_data = json.dumps({

"receipt": {

"items": [

{

"description": "Название",

"quantity": 1,

"amount": {

"value": price_rub,

"currency": CURRENCY

},

"vat_code": 1,

"payment_mode": "full_payment",

"payment_subject": "service"

}

]

}

})

async def buy(message: types.Message):

    await message.bot.send_invoice(
    chat_id=message.chat.id,
    title='Подписка на бота на 1 месяц',
    description='Активация подписки',
    provider_token=config.pay_set.payments_token,
    currency=CURRENCY,
    prices=[PRICE],
    need_email=True,
    send_email_to_provider = True,
    start_parameter='one-month-subscription',
    provider_data=provider_data,
    payload=f'sub_30days_{message.from_user.id}'  # ✅ Уникальный payload
)
