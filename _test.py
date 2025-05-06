from services.base_service import ServiceDB
from services.operator_service import OperatorService
import os
import sys


#test = ServiceDB()
operator = OperatorService()


operator.create_product(price=5000)




#print([file for file in os.listdir() if file.endswith(".py")])