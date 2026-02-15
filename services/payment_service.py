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

"description": "Подиска на 1 месяц",

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
    description='Каждый день мы пишем 30 сказок для разных возрастов ✏️ Подписываясь на 1 месяц ты получишь доступ к ❗️900❗️ сказкам за период подписки!',
    provider_token=config.pay_set.payments_token,
    currency=CURRENCY,
    prices=[PRICE],
    need_email=True,
    send_email_to_provider = True,
    is_flexible=False,
    start_parameter='one-month-subscription',
    provider_data=provider_data,
    payload=f'sub_30days_{message.from_user.id}',
    # photo_url="AgACAgIAAxkBAAFCa5RpkGmdZIP7Kmv04J8GmIML0SlreAACXhZrGyHSgUh7WTjxSIGt3AEAAwIAA3gAAzoE",
    photo_url='https://sun9-12.userapi.com/s/v1/ig2/elIxpfzPJYbuQQuf7kcWaX8B-W2Stw4gEuPPQT-baBQF_EWdo9yk9LvmaFvDJOYI2uAZLzSGBVVrKvMDltANXnWa.jpg?quality=95&as=32x32,48x48,72x72,108x108,160x160,240x240,360x360,480x480,540x540,640x640,720x720,1080x1080,1280x1280,1440x1440,2048x2048&from=bu&u=JGYCoILlHrRoYvB2DXLpqaa185FWv7YZN_UuS5WWFwI&cs=640x0',
    photo_size=568806,
    photo_height=2048,
    photo_width=2048
)
