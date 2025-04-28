import functools
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


def with_session(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        from services.database.database import Session as LocalSession
        with LocalSession() as session:
            try:
                if 'session' in func.__code__.co_varnames:
                    kwargs['session'] = session 

                logger.info("Сессия запущена.")
                res = func(self, *args, **kwargs)

                if res is None:
                    session.commit()
                logger.info("Сессия успешно завершилась.")
                return res
            except Exception as err:
                session.rollback()
                logger.error(f"Во время сесси возникла ошибка {err}.")
    return wrapper