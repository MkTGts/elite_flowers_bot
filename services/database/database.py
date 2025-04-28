from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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


try:
    engine = create_engine("sqlite:///data/db/app.db", echo=True)
    Session = sessionmaker(bind=engine)
except Exception as err:
    logger.error(f"Во время подключения к бд или создания сессии возникла ошибка {err}")