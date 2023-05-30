import os

from aiogram import Bot

from bot.handlers import db


async def send_message_interval(bot: Bot):
    await bot.send_message(
        chat_id=os.getenv("ADMIN_ID"),
        text="Это сообщение будет оптравляться с каким-то интервалом",
    )


async def notify(bot: Bot):
    users = db.get_users_list()
