from services.base_service import ServiceDB
from services.operator_service import OperatorService
from services.user_service import UserService
import os
import sys
import re


#test = ServiceDB()
operator = OperatorService()


operator.create_product(price=3400)



#print([file for file in os.listdir() if file.endswith(".py")])