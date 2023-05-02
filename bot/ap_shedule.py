import os

from aiogram import Bot


async def send_message_interval(bot: Bot):
    await bot.send_message(
        chat_id=os.getenv("USER_ID"),
        text="Это сообщение будет оптравляться с интервалом в 10 секунд",
    )
