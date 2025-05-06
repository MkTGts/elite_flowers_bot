from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXCON_USER_KEYBOARDS, LEXICON_OPERATOR_KEYBOARDS


operator_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(
            text=LEXICON_OPERATOR_KEYBOARDS["show_orders"],
            callback_data="operator_but_show_orders")], 
                      [
        InlineKeyboardButton(
            text=LEXICON_OPERATOR_KEYBOARDS["show_product"],
            callback_data="operator_but_show_product")],
                      [
        InlineKeyboardButton(
            text=LEXICON_OPERATOR_KEYBOARDS["add_product"],
            callback_data="operator_but_add_product")],
                      [
        InlineKeyboardButton(
            text=LEXICON_OPERATOR_KEYBOARDS["drop_product"],
            callback_data="operator_but_drop_product")],
                      [
        InlineKeyboardButton(
            text=LEXICON_OPERATOR_KEYBOARDS["show_users"],
            callback_data="operator_but_show_users")],
            ])














