from services.database.database import engine 
from services.database.models import Base
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


def init_db():
    Base.metadata.create_all(engine)
    logger.info("База данных инициализирована. Таблицы созданы.")


if __name__ == "__main__":
    try:
        init_db()
    except Exception as err:
        logger.error(f"Во время инициализации базы данных возникла ошибка {err}")