from .base_service import ServiceDB
from services.decorators import with_session
from sqlalchemy.orm import Session
from services.database.models import Operator, Product
import logging


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



class OperatorService(ServiceDB):
    def __init__(self):
        super().__init__()


    @with_session
    def create_product(self, session: Session, price: int):
        '''Метод добавления оператором букета'''
        new_product = Product(
            price=price
        )
        session.add(new_product)