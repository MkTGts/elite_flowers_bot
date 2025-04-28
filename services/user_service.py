from .base_service import ServiceDB
from services.decorators import with_session
from sqlalchemy.orm import Session
from services.database.models import User
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


class UserService(ServiceDB):
    def __init__(self):
        super().__init__()