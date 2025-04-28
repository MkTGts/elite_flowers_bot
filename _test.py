from services.base_service import ServiceDB


test = ServiceDB()



for i in test._return_orders(tg_id=3):
    print(i.status, i.user_id)