import asyncio
import os

from aiogram import Dispatcher, Bot
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from app.handlers.admin_panel import user_list, add_food, orders_list, edit_food, settings, requests_for_access
from app.handlers.guest_panel import access
from app.handlers.user_panel import start, cart, order, menu
from app.middlewares.db import DbSessionMiddleware
from app.utils import bot

load_dotenv()
DB_URL = os.getenv('DB_URL')
TOKEN = os.getenv('TOKEN')


async def main():
    engine = create_async_engine(url=DB_URL, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.include_routers(start.router,
                       menu.router,
                       cart.router,
                       order.router,
                       settings.router,
                       access.router,
                       edit_food.router,
                       add_food.router,
                       user_list.router,
                       requests_for_access.router,
                       orders_list.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
