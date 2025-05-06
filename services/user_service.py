from .base_service import ServiceDB
from services.decorators import with_session
from sqlalchemy.orm import Session
from services.database.models import User, Order, Product
import logging
from .services import _now_date


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


class UserService(ServiceDB):
    def __init__(self):
        super().__init__()


    @with_session
    def create_order(self, session: Session, tg_id: int, 
                     product_id, 
                     delivery: str,
                     adress: str,
                     status: str,
                     total: int):
        '''Создание заказа пользователем'''
        new_order = Order(
            user_id=session.query(User).filter(User.tg_id==tg_id).first.user_id,
            product_id=product_id,
            delivery=delivery,
            adress=adress,
            status=status,
            date=_now_date(),
            total=total
        )
        session.add(new_order)


    @with_session
    def show_orders(self, session: Session, tg_id: int):
        '''Просмотр списк своих заказов пользователем'''
        user_id = session.query(User).filter(User.tg_id==tg_id).first().user_id
        return session.query(Order).filter(Order.user_id==user_id).all()