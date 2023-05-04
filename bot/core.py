import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.models import DBase

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s:%(lineno)d:%(levelname)s:[%(asctime)s] - %(name)s - %(message)s",
)

# Initialize bot, storage, database and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DBase()
sheduler = AsyncIOScheduler()


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message, db=db):
    """
    This handler will be called when user sends `/start` command
    """
    db.add_user(message.from_user.values)
    await message.reply(
        "Hi!\nI'm OrangeBot!\nNow you can subscribe to Github users repo updates"
    )


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == "__main__":
    sheduler.start()
    executor.start_polling(dp, skip_updates=True)
