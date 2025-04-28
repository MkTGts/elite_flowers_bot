import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from data.config import Config, load_config
from handlers import user_handlers, other_handlers, operator_handlers


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="logs.log",
    filemode="a",
    encoding="utf-8",
    format= '[%(asctime)s] #%(levelname)-8s %(filename)s:'
       '%(lineno)d - %(name)s - %(message)s'
)


async def main():
    logger.info("Старт бота.") 

    config: Config = load_config()  

    bot = Bot(  
        token=config.tg_bot.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher() 


    dp.include_router(other_handlers.router)
    

    await bot.delete_webhook(drop_pending_updates=True)  
    await dp.start_polling(bot)  


try:
    asyncio.run(main())
except Exception as err:
    logger.critical(f"Stop! Error {err}")