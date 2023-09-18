import asyncio
import os

from aiogram import Dispatcher
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.handlers import start
from app.handlers.admin_panel import add_item, edit_item
from app.handlers.user_panel import item_list
from app.middlewares.db import DbSessionMiddleware
from app.utils import bot

load_dotenv()
DB_URL = os.getenv('DB_URL')


async def main():
    engine = create_async_engine(url=DB_URL, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.include_routers(start.router,
                       item_list.router,
                       add_item.router,
                       edit_item.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
