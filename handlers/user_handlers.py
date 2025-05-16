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
    waiting_date_delivery = State()
    waiting_address_delivery = State()


@router.callback_query(IsUser(), F.data.in_("user_but_show_orders"))
async def process_user_show_orders(callback: CallbackQuery):
    try:
        await callback.message.answer(
            text="\n\n".join([
                f"ID заказа: {order.order_id}\nЗаказ: Букет №{order.product_id}\nДоставка: {order.delivery}\nАдресс: {order.adress}\nСтатус: {order.status}\nДата заказа: {order.date}\nДата получения: {order.date_delivery}\nСумма: {order.total} руб."
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
async def perocess_user_create_order_ok_select_date_delivery(callback: CallbackQuery):
    try:
        n = re.findall(r"\d+", callback.data)[0]

        await callback.message.answer(
            text=LEXCON_USER_HANDLERS["select_date_deivery"],
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text="Ближайшее время",
                        callback_data=f"user_select_product_deliv_blij{n}"
                    )],
                    [InlineKeyboardButton(
                        text="Ввести дату",
                        callback_data=f"user_select_product_deliv_other{n}"
                    )],
            ])
        )
        cache[callback.from_user.id] = {
            "num_buketa": n
        }
        logger.info((f"Выбор даты получения заказа. Пользователь {callback.message.from_user.id} {callback.message.from_user.full_name} {callback.message.from_user.username}"))
    except Exception as err:
        logger.error(f"Во время выбора времени ошибка {err}. Пользователь {callback.message.from_user.id} {callback.message.from_user.full_name} {callback.message.from_user.username}")

    await callback.answer()



@router.callback_query(F.data.regexp(r"user_select_product_deliv_other"))
async def process_user_create_order_custom_date_delivery(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.answer(
            text="Введите желаемую дату заказа"
        )
        await state.set_state(UserCreateOrder.waiting_date_delivery)
    except Exception as err:
        logger.error(f"Не выходит сообщение о просьбе ввести дату: {err}. Пользователь {callback.message.from_user.id} {callback.message.from_user.full_name} {callback.message.from_user.username}")

    await callback.answer()



async def perocess_user_create_order_ok(event: CallbackQuery | Message):
    try:
        if isinstance(event, CallbackQuery):
            await event.message.answer(
            text=LEXCON_USER_HANDLERS["order_with_delivery"],
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text=LEXCON_USER_HANDLERS["deliv"],
                        callback_data=f"user_select_product_deliv"
                    )],
                    [InlineKeyboardButton(
                        text=LEXCON_USER_HANDLERS["samo"],
                        callback_data=f"user_select_product_samo"
                    )],
            ])
        )
            await event.answer()

        else:
            await event.answer(
            text=LEXCON_USER_HANDLERS["order_with_delivery"],
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text=LEXCON_USER_HANDLERS["deliv"],
                        callback_data=f"user_select_product_deliv"
                    )],
                    [InlineKeyboardButton(
                        text=LEXCON_USER_HANDLERS["samo"],
                        callback_data=f"user_select_product_samo"
                    )],
            ])
        )

    except Exception as err:
        logger.error(f"Во время выбора доставки или самовывоза ошибка {err}.")




@router.callback_query(IsUser(), (F.data.regexp(r"user_select_product_deliv_blij")))
async def delivery_date_blij(callback: CallbackQuery):
    try:
        cache[callback.from_user.id].update({
                "date_delivery": "Ближайшее"
            }
        )
        await perocess_user_create_order_ok(event=callback)
        logger.info((f"Выбор даты получения - Ближайшее. Пользователь {callback.message.from_user.id} {callback.message.from_user.full_name} {callback.message.from_user.username}"))
    except Exception as err:
        logger.error(f"Не удалось применить дату получение - Ближайшее: {err}. Пользователь {callback.message.from_user.id} {callback.message.from_user.full_name} {callback.message.from_user.username}")
    
    await callback.answer()


@router.message(IsUser(), UserCreateOrder.waiting_date_delivery)
async def delivery_date_custom(message: Message, state: FSMContext):
    try:
        cache[message.from_user.id].update({
                "date_delivery": message.text
            }
        )

        await perocess_user_create_order_ok(event=message)
        logger.info((f"Выбор даты получения - Кастомный. Пользователь {message.from_user.id} {message.from_user.full_name} {message.from_user.username}"))
    except Exception as err:
        logger.error(f"Не удалось применить дату получение - Кастомный: {err}. Пользователь {message.from_user.id} {message.from_user.full_name} {message.from_user.username}")
    await state.clear()





@router.callback_query(IsUser(), F.data.regexp(r"user_select_product_samo"))
async def perocess_user_create_order_samo(callback: CallbackQuery):
    try:
        n = cache[callback.from_user.id]["num_buketa"]
        user.create_order(
            tg_id=int(callback.from_user.id),
            product_id=n,
            delivery="<b>Самовывоз</b>",
            status="Не оплачен",
            date_delivery=cache[callback.from_user.id]["date_delivery"],
            total=cache[int(n)]["price"]
        )
        
        await callback.message.answer(
            text=LEXCON_USER_HANDLERS["create_order_samo"],
            reply_markup=user_inline_kb
        )

        logger.info(f"Создан заказ на самовывоз. Пользователь {callback.message.from_user.id} {callback.message.from_user.full_name} {callback.message.from_user.username}")
        cache[callback.from_user.id] = {}

    
    except Exception as err:
        logger.error(f"Во время создания заказа на самовывоз ошибка {err}. Пользователь {callback.message.from_user.id} {callback.message.from_user.full_name} {callback.message.from_user.username}")

    await callback.answer()

    
@router.callback_query(IsUser(), F.data.regexp(r"user_select_product_deliv"))
async def perocess_user_create_order_deliv(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.answer(
            text=LEXCON_USER_HANDLERS["input_address_deliv"]
        )
        await state.set_state(UserCreateOrder.waiting_address_delivery)

        logger.info(f"Запрашиваться адрес доставки. Пользователь {callback.message.from_user.id} {callback.message.from_user.full_name} {callback.message.from_user.username}")
    except Exception as err:
        logger.error(f"Во время запроса адреса доствки: {err}. Пользователь {callback.message.from_user.id} {callback.message.from_user.full_name} {callback.message.from_user.username}")

    await callback.answer()


@router.message(IsUser(), UserCreateOrder.waiting_address_delivery)
async def perocess_user_create_order_deliv_in(message: Message, state: FSMContext):
    try:
        n = cache[message.from_user.id]["num_buketa"]
        user.create_order(
            tg_id=int(message.from_user.id),
            product_id=n,
            delivery="<b>Доставка</b>",
            status="Не оплачен",
            date_delivery=cache[message.from_user.id]["date_delivery"],
            adress=message.text,
            total=cache[int(n)]["price"]
        )
        
        await message.answer(
            text=LEXCON_USER_HANDLERS["create_order_deliv"],
            reply_markup=user_inline_kb
        )
        cache[message.from_user.id] = {}

        logger.info(f"Создается заказ на доставку. Пользователь {message.from_user.id} {message.from_user.full_name} {message.from_user.username}")
    except Exception as err:
        logger.error(f"Адрес доставки не принят: {err}. Пользователь {message.from_user.id} {message.from_user.full_name} {message.from_user.username}")
