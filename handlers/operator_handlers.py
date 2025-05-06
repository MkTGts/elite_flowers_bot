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
async def process_operator_show_orders(message: Message):
    pass


@router.callback_query(IsOperator(), F.data.in_("operator_but_show_product"))
async def process_operator_show_product(message: Message):
    pass


@router.callback_query(IsOperator(), F.data.in_("operator_but_add_product"))
async def process_operator_add_product(message: Message):
    pass


@router.callback_query(IsOperator(), F.data.in_("operator_but_drop_product"))
async def process_operator_drop_product(message: Message):
    pass


@router.callback_query(IsOperator(), F.data.in_("operator_but_show_users"))
async def process_operator_show_users(message: Message):
    pass

