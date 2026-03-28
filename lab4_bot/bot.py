import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.engine import create_db

from handlers.user import user_router
from handlers.admin import admin_router

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    await create_db()
    print("✅ Database initialized successfully!")

    dp.include_router(admin_router)
    dp.include_router(user_router)

    await bot.delete_webhook(drop_pending_updates=True)

    print("🚀 The bot is launched and ready to work!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 The bot was stopped manually.")