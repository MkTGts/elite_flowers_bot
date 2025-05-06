from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXCON_USER_KEYBOARDS


user_but_show_orders = InlineKeyboardButton(
    text=LEXCON_USER_KEYBOARDS["show_orders"],
    callback_data="user_but_show_orders"
)

user_but_create_order = InlineKeyboardButton(
    text=LEXCON_USER_KEYBOARDS["create_order"],
    callback_data="user_but_create_order"
)

user_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[[user_but_create_order], [user_but_show_orders]]
)














