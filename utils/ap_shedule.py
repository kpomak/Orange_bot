# import os

from aiogram import Bot

from bot.handlers import db


# async def send_message_interval(bot: Bot):
#     await bot.send_message(
#         chat_id=os.getenv("ADMIN_ID"),
#         text="Это сообщение будет оптравляться с каким-то интервалом",
#     )


async def notify(bot: Bot):
    updates = db.check_updates()
    for update in updates:
        await bot.send_message(
            chat_id=update["subscriber"],
            text=f"Repo {update['repo']} was updated!\n{update['url']}",
        )
