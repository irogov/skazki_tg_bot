from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON_RU

button_1 = KeyboardButton(text=LEXICON_RU['1'])
button_2 = KeyboardButton(text=LEXICON_RU['2'])
button_3 = KeyboardButton(text=LEXICON_RU['3'])

age_keyboard_builder = ReplyKeyboardBuilder()
age_keyboard_builder.row(button_1, button_2, button_3, width=3)
age_keyboard = age_keyboard_builder.as_markup(resize_keyboard=True)