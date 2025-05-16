from aiogram.utils.markdown import hlink


LEXICON_RU: dict[str, str] = {
    "/start": 'Привет.',
    "/help": "Еще заполняется",
    "no_reg": "Не зарегистрирован.\nНеобходимо пройти регистрацю.",
    "name_req": "Введите ваше имя",
    "phone_req": "Введите ваш номер телефона",
    "reg_ok": "Процесс регистрации завершился успешно"
   }


LEXCON_USER_KEYBOARDS: dict[str, str] = {
    "show_orders": "Список моих заказов",
    "create_order": "Сделать заказ",
    "pay_order": "Оплатить заказ"
}

LEXICON_ORDER_STATUS: dict[str, str] = {
    "no_pay": "Не оплачен",
    "paid": "Оплачен"
}

LEXCON_USER_HANDLERS: dict[str, str] = {
    "welcome": "Приветсвие пользователя",
    "products_list_for_create_prder": "Выберите букет для заказа",
    "order_no": "Отмена создания заказа\n\nГлавное меню",
    "order_with_delivery": "Доставка или самовывоз",
    "deliv": "Доставка",
    "samo": "Самовывоз",
    "select_date_deivery": "Когда хотите получить заказ?",
    "create_order_samo": "Заказ создан",
    "create_order_deliv": "Заказ создан",
    "input_address_deliv": "Введите адрес доставки",
    "select_pay_order": "Заказ можно оплатить переводом по номеру <b>+7999-999-99-99 Ф. Имя Отчество</b>\nПосле оплаты, нажмите кнопку Оплатил, менджер проверит информаци и статус заказа либо иземниться, либо менеджер с вами свяжется.",
    "user_say_that_paid": "Информация об оплате проверяется.",
    "user_say_dont_paid": "Возврат в основное меню"
}


LEXICON_OPERATOR_KEYBOARDS: dict[str, str] = {
    "show_orders": "Список заказов",
    "edit_status_orders": "Изменить статус заказа",
    "show_product": "Список букетов",
    "add_product": "Добавить букет",
    "drop_product": "Удалить букет",
    "show_users": "Список пользователей"
}

LEXCON_OPERATOR_HANDLERS: dict[str, str] = {
    "welcome": "Приветсвие оператора"
}

 
