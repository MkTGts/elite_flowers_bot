from services.base_service import ServiceDB
from services.operator_service import OperatorService
from services.user_service import UserService
import os
import sys
import re


#test = ServiceDB()
operator = OperatorService()


operator.create_product(price=4300)

user = UserService()

user.create_order(
    tg_id=123,
    product_id=5,
    delivery="Самовывоз",
    status="Не оплачен",
    total=32112312,

)


#print([file for file in os.listdir() if file.endswith(".py")])