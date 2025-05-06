import logging
import os
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon import LEXICON_RU, LEXCON_USER_HANDLERS
from services.database.models import User
from services.user_service import UserService
from keyboards.kyboards_users import user_inline_kb
from filters.filters import IsUser





# инициализация логгера
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="logs.log",
    filemode="a",
    encoding="utf-8",
    format= '[%(asctime)s] #%(levelname)-8s %(filename)s:'
       '%(lineno)d - %(name)s - %(message)s'
)


user = UserService()
router = Router()

class UserCreateOrder(StatesGroup):
    waiting_user_name = State()
    waiting_phone_number = State()


@router.callback_query(IsUser(), F.data.in_("user_but_show_orders"))
async def process_user_show_orders(callback: CallbackQuery):
    await callback.message.answer(
        text="Список заказов",#"\n\n".join([
            #f"ID заказа: {order.product_id}\nДоставка: {order.delivery}\nСтатус: {order.status}\nДата: {order.date}\nСумма: {order.total}"
            #for order in user.show_orders(tg_id=callback.from_user.id)
        #]),
        reply_markup=user_inline_kb
    )
    await callback.answer()


@router.callback_query(IsUser(), F.data.in_("user_but_create_order"))
async def process_user_select_for_create_order(callback: CallbackQuery):
    for product in user._return_products():
        #with open(f"photo{product.product_id}.jpg", "rb") as img:
        await callback.message.answer_photo(
            photo=FSInputFile(f"./photo/photo{product.product_id}.jpg"),
            caption=f"Букет {product.product_id}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text=f"Букет {product.product_id}",
                    callback_data=f"user_select_product{product.product_id}"
                )]
            ])
        )

    await callback.answer()


@router.callback_query(IsUser(), F.data.regexp(r"user_select_product\d+$"))
async def process_user_create_order(callback: CallbackQuery):


    await callback.answer()