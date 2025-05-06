import logging
import re
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
cache = {}

class UserCreateOrder(StatesGroup):
    waiting_user_name = State()
    waiting_phone_number = State()


@router.callback_query(IsUser(), F.data.in_("user_but_show_orders"))
async def process_user_show_orders(callback: CallbackQuery):
    try:
        await callback.message.answer(
            text="\n\n".join([
                f"ID заказа: {order.product_id}\nДоставка: {order.delivery}\nСтатус: {order.status}\nДата: {order.date}\nСумма: {order.total}"
                for order in user.show_orders(tg_id=callback.from_user.id)
            ]),
            reply_markup=user_inline_kb
        )
        logger.info(f"Список заказов запросил пользователь {callback.message.from_user.id} {callback.message.from_user.full_name} {callback.message.from_user.username}")
    except Exception as err:
        logger.error(f"Во время вывода списка заказов, возникла ошибка {err}.Пользователь {callback.message.from_user.id} {callback.message.from_user.full_name} {callback.message.from_user.username}")
        
    await callback.answer()


@router.callback_query(IsUser(), F.data.in_("user_but_create_order"))
async def process_user_select_for_create_order(callback: CallbackQuery):
    try:
        for product in user._return_products():
            await callback.message.answer_photo(
                photo=FSInputFile(f"./photo/photo{product.product_id}.jpg"),
                caption=f"Букет №{product.product_id}\nЦена: {product.price} руб.",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text=f"Букет №{product.product_id}",
                        callback_data=f"user_select_product{product.product_id}"
                    )]
                ])
            )
            cache.update({product.product_id: {"price": product.price}})
        logger.info(f"Начал создавать заказ пользователь {callback.message.from_user.id} {callback.message.from_user.full_name} {callback.message.from_user.username}")
    except Exception as err:
        logger.error(f"Во время начала создания заказа, возникла ошибка {err}.Пользователь {callback.message.from_user.id} {callback.message.from_user.full_name} {callback.message.from_user.username}")

    print(cache)
    await callback.answer()


@router.callback_query(IsUser(), F.data.regexp(r"user_select_product\d+$"))
async def process_user_create_order_conf(callback: CallbackQuery):
    n = re.findall(r"\d+", callback.data)[0]

    await callback.message.answer(
        text="\n\nПроцесс создания заказа",
        reply_to_message_id=callback.message.message_id
    )

    await callback.message.answer_photo(
        photo=FSInputFile(f"./photo/photo{n}.jpg"),
        caption=f"Выбран букет №{n}\nЦена: {cache[int(n)]["price"]} руб.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text=f"Все верно",
                    callback_data=f"user_select_product{n}_ok"
                )],
                [InlineKeyboardButton(
                    text=f"Отменить заказ",
                    callback_data=f"user_select_product{n}_no"
                )],
        ])
    )
    
    await callback.answer()


@router.callback_query(IsUser(), F.data.regexp(r"user_select_product\d+_no"))
async def perocess_user_create_order_no(callback: CallbackQuery):
    await callback.message.answer(
        text=LEXCON_USER_HANDLERS["order_no"],
        reply_markup=user_inline_kb
    )

    await callback.answer()


@router.callback_query(IsUser(), F.data.regexp(r"user_select_product\d+_ok"))
async def perocess_user_create_order_ok(callback: CallbackQuery):
    try:
        n = re.findall(r"\d+", callback.data)[0]

        await callback.message.answer(
            text=LEXCON_USER_HANDLERS["order_with_delivery"],
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text=LEXCON_USER_HANDLERS["deliv"],
                        callback_data=f"user_select_product_deliv{n}"
                    )],
                    [InlineKeyboardButton(
                        text=LEXCON_USER_HANDLERS["samo"],
                        callback_data=f"user_select_product_samo{n}"
                    )],
            ])
        )
    except Exception as err:
        logger.error(f"Во время выбора доставки или самовывоза ошибка {err}. Пользователь {callback.message.from_user.id} {callback.message.from_user.full_name} {callback.message.from_user.username}")

    await callback.answer()


@router.callback_query(IsUser(), F.data.regexp(r"user_select_product_samo\d+"))
async def perocess_user_create_order_samo(callback: CallbackQuery):
    try:
        n = int(re.findall(r"\d+", callback.data)[0])
        user.create_order(
            tg_id=int(callback.from_user.id),
            product_id=n,
            delivery="Самовывоз",
            status="Не оплачен",
            total=cache[int(n)]["price"]
        )
        
        await callback.message.answer(
            text=LEXCON_USER_HANDLERS["create_order_samo"],
            reply_markup=user_inline_kb
        )

        logger.info(f"Создан заказ на самовывоз. Пользователь {callback.message.from_user.id} {callback.message.from_user.full_name} {callback.message.from_user.username}")
    

    
    except Exception as err:
        logger.error(f"Во время создания заказа на самовывоз ошибка {err}. Пользователь {callback.message.from_user.id} {callback.message.from_user.full_name} {callback.message.from_user.username}")

    await callback.answer()