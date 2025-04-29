import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON_RU, LEXCON_USER_HANDLERS, LEXCON_OPERATOR_HANDLERS
from services.base_service import ServiceDB
from keyboards.kyboards_users import user_inline_kb
from keyboards.kyboards_operators import operator_inline_kb


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="logs.log",
    filemode="a",
    encoding="utf-8",
    format= '[%(asctime)s] #%(levelname)-8s %(filename)s:'
       '%(lineno)d - %(name)s - %(message)s'
)


base = ServiceDB()
router = Router()
cache = {}



class UserRegistartion(StatesGroup):
    waiting_user_name = State()
    waiting_phone_number = State()



@router.message(Command(commands="start"))
async def proccess_command_start(message: Message, state: FSMContext):
    try:
        if base._check_role(tg_id=message.from_user.id) == "operator":
            await message.answer(
                text=LEXCON_OPERATOR_HANDLERS["welcome"],
                reply_markup=user_inline_kb
            )
            logger.info(f"Авторизовался через СТАРТ оператор {message.from_user.id} {message.from_user.full_name} {message.from_user.username}")


        elif base._check_role(tg_id=message.from_user.id) == "user":
            await message.answer(
                text=LEXCON_USER_HANDLERS["welcome"],
                reply_markup=operator_inline_kb
            )
            logger.info(f"Авторизовался через СТАРТ пользователь {message.from_user.id} {message.from_user.full_name} {message.from_user.username}")

        else:
            await message.answer(
                text=LEXICON_RU["no_reg"]
            )
            await message.answer(
                text=LEXICON_RU["name_req"]
            )
            await state.set_state(UserRegistartion.waiting_user_name)
            logger.info(f"Запущена регистрация пользователя {message.from_user.id} {message.from_user.full_name} {message.from_user.username}")
    except Exception as err:
        await message.answer(
            text="Что-то пошло не так."
        )
        logger.error(f"Возникла ошибка {err} на команде СТАРТ. Пользователь {message.from_user.id} {message.from_user.full_name} {message.from_user.username}")


@router.message(UserRegistartion.waiting_user_name)
async def user_registration_step_name(message: Message, state: FSMContext):
    try:
        cache[message.from_user.id] = {"fullname": message.text}
        state.clear()
        await state.set_state(UserRegistartion.waiting_phone_number)
        await message.answer(
            text=LEXICON_RU["phone_req"]
        )
        logger.info(f"Процесс регистрации. Принято и записано в кэш полное имя {message.text}.\
Пользователь {message.from_user.id} {message.from_user.full_name} {message.from_user.username}")

    except Exception as err:
        await state.clear()
        await message.answer(
            text="Возникли проблемы...\nОбратитесь к администратору."
        )
        
        logger.error(f"Процесс регистрации. На стадии ввода полного имени возникла ошибка {err}. \
Пользователь {message.from_user.id} {message.from_user.full_name} {message.from_user.username}")
        
       
@router.message(UserRegistartion.waiting_phone_number)
async def user_registaration_step_phone(message: Message, state: FSMContext):
    try:
        cache[message.from_user.id].update({
                "phone_number": message.text,
                "username": message.from_user.username
                })
        print(cache)
        base.users_registration(tg_id=message.from_user.id, data=cache[message.from_user.id])
        await state.clear()
        await message.answer(
            text=LEXICON_RU["reg_ok"]
        )

        logger.info(f"Процесс регистрации. Принят и записан в кэш номер тел {message.text}. \
Зарегистрирован пользователь {message.from_user.id} {message.from_user.full_name} {message.from_user.username}")
        
    except Exception as err:
        await state.clear()
        await message.answer(
            text="Возникли проблемы...\nОбратитесь к администратору."
        )

        logger.error(f"Процесс регистрации. На стадии ввода номера тел возникла ошибка {err}. \
Пользователь {message.from_user.id} {message.from_user.full_name} {message.from_user.username}")




@router.message(F.text.lower() == "my phone num")
async def test_phone_number(message: Message):
    await message.answer(
        text="Поделиться контактами",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Поделиться контактами", request_contact=True)]
            ],
            resize_keyboard=True
        )
    )


@router.message(F.contact)
async def return_phone_number(message: Message):
    contact = message.contact.phone_number
    await message.answer(text=f"Ваш номер {contact}", reply_markup=ReplyKeyboardRemove())
    




    
