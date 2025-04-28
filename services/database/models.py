from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    username = Column(String)
    fullname = Column(String)
    phone_number = Column(String)


class Operator(Base):
    __tablename__ = "operators"

    operator_id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    username = Column(String)
    fullname = Column(String)


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    photo = Column(String)
    price = Column(Integer)


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    delivery = Column(String)
    adress = Column(String)
    status = Column(String)
    total = Column(Integer)

    