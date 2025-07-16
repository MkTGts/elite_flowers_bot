import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON_RU, LEXCON_OPERATOR_HANDLERS
from services.operator_service import OperatorService
from keyboards.kyboards_operators import operator_inline_kb
from filters.filters import IsOperator


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="logs.log",
    filemode="a",
    encoding="utf-8",
    format= '[%(asctime)s] #%(levelname)-8s %(filename)s:'
       '%(lineno)d - %(name)s - %(message)s'
)


operator = OperatorService()
router = Router()


@router.callback_query(IsOperator(), F.data.in_("operator_but_show_orders"))
async def process_operator_show_orders(callback: CallbackQuery):
    try:
        pass
    except Exception as err:
        logger.error(f"Во время просмотра оператором списка заказов, возникла ошибка {err}")

    await callback.answer()


@router.callback_query(IsOperator(), F.data.in_("operator_but_edit_order_status"))
async def process_operator_edit_order_status(callback: CallbackQuery):
    try:
        pass
    except Exception as err:
        logger.error(f"Во время нажатия кнопки изменения статуса заказа оператором, возникла ошибка {err}")
        pass

    await callback.answer()


@router.callback_query(IsOperator(), F.data.in_("operator_but_show_product"))
async def process_operator_show_product(callback: CallbackQuery):
    try:
        pass
    except Exception as err:
        logger.error(f"о время нажатия кнопки просмотра списка продуктов оператором, возникла ошибка {err}")
        pass

    await callback.answer()


@router.callback_query(IsOperator(), F.data.in_("operator_but_add_product"))
async def process_operator_add_product(callback: CallbackQuery):
    try:
        pass
    except Exception as err:
        logger.error(f"Во время нажатия кнопки добавления продукта оператором, возникла ошибка {err}")
        pass

    await callback.answer()


@router.callback_query(IsOperator(), F.data.in_("operator_but_drop_product"))
async def process_operator_drop_product(callback: CallbackQuery):
    try:
        pass
    except Exception as err:
        logger.error(f"Во время нажатия кнопки удаления продукта оператором, возникла ошибка {err}")
        pass

    await callback.answer()


@router.callback_query(IsOperator(), F.data.in_("operator_but_show_users"))
async def process_operator_show_users(callback: CallbackQuery):
    try:
        pass
    except Exception as err:
        logger.error(f"Во премя нажатия кнопки просмотра списка пользователей оператором, возникла ошибка {err}")
        pass

    await callback.answer()

