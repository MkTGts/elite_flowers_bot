from services.decorators import with_session
from sqlalchemy.orm import Session
from services.database.models import User, Product, Order, Operator
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="logs.log",
    filemode="a",
    encoding="utf-8",
    format= '[%(asctime)s] #%(levelname)-8s %(filename)s:'
       '%(lineno)d - %(name)s - %(message)s'
)


class ServiceDB:
    @with_session
    def _check_role(self, session: Session, tg_id: int):
        '''Определяет роль пользователя'''
        try:
            if session.query(Operator).filter(Operator.tg_id == tg_id).first():
                logger.info(f"Найден оператор с tg_id={tg_id}")
                return "operator"
            
            elif session.query(User).filter(User.tg_id == tg_id).first():
                logger.info(f"Найден пользователь с tg_id={tg_id}")
                return "user"
            
            logger.info(f"Старт отправил незарегистрированный пользователь TG ID {tg_id}")
            return None
        except Exception as err:
            logger.error(f"Ошибка при старте на стадии определения роли {err}")
            


    @with_session
    def _return_users(self, session: Session, 
                      tg_id: int|None=None,
                      ):
        '''Возвращает список всех пользователей, или находит пользователя по tg_id'''
        if tg_id:
            return session.query(User).filter(User.tg_id==tg_id).first()
        else:
            return session.query(User).all()
        

    @with_session
    def _return_products(self, session: Session, 
                        product_id: int|None=None
                        ):
        '''Возвращает список всех товаров, или находит по id'''
        if product_id:
            return session.query(Product).filter(Product.product_id==product_id).first()
        else:
            return session.query(Product).all()
        

    @with_session
    def _return_orders(self, session: Session,
                       tg_id: int|None=None
                       ):
        '''Возвращает список заказов или находит заказ по tg_id'''
        if tg_id is None:
            print(1)
            return session.query(Order).all()
        else:
            print(2)
            user_id = session.query(User).filter(User.tg_id==tg_id).first().user_id
            return session.query(Order).filter(Order.user_id==user_id).all()
        

    @with_session
    def _return_operators(self, session: Session):
        '''Возвращает список всех операоров'''
        return session.query(Operator).all()
    

    @with_session
    def users_registration(self, session: Session, tg_id: int, data: dict):
        try:
            new_user = User(
                tg_id=tg_id,
                username=data["username"],
                fullname=data["fullname"],
                phone_number=data["phone_number"]
            )
            session.add(new_user)

            logger.info("Метод регистрации отработал успешно.")

        except Exception as err:
            logger.error(f"Во время работы метода регистрации возникла ошибка {err}")