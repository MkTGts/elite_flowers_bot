from services.decorators import with_session
from sqlalchemy.orm import Session
from services.database.models import User, Product, Order, Operator


class ServiceDB:
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
        