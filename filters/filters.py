from services.base_service import ServiceDB
from aiogram.filters import BaseFilter
from aiogram.types import Message


base = ServiceDB()

class IsUser(BaseFilter):
    '''Проверка что пользователь в базе и является обычным пользователем'''
    async def __call__(self, message: Message):
        return base._check_role(tg_id=message.from_user.id) == "user"


class IsOperator(BaseFilter):
    '''Проверка что пользователь есть в базе и является оператором'''
    async def __call__(self, message: Message):
        return base._check_role(tg_id=message.from_user.id) == "operator"
