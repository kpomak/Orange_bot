import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.handlers import register_all_handlers

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s:%(lineno)d:%(levelname)s:[%(asctime)s] - %(name)s - %(message)s",
)

# Initialize bot, storage, sheduler and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
sheduler = AsyncIOScheduler()

# Register handlers
register_all_handlers(dp)


if __name__ == "__main__":
    sheduler.start()
    executor.start_polling(dp, skip_updates=True)
