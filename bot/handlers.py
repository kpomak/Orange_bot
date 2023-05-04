from aiogram import types

from bot.models import DBase

# from bot.core import dp

db = DBase()


async def echo(message: types.Message):
    """
    Simple echo handler
    """
    await message.answer(message.text)


async def send_welcome(message: types.Message, db=db):
    """
    This handler will be called when user sends `/start` command
    """
    db.add_user(message.from_user.values)
    await message.reply(
        f"Hi!\nI'm OrangeBot! 🍊\n"
        f"Now you can subscribe to updates of Github users 🙌\n"
        f"Send /help for more 🍊"
    )


async def send_help(message: types.Message):
    """
    This handler will be called when user sends `/help` command
    """
    answer = (
        f"Hola!\nSoy un BotNaranja! 🍊\n"
        f"I will send to you information about updates of Github repositories.\n\n"
        f"Register with /start command first.\n"
        f"Then you can /subscribe to github users and /unsubscribe.\n"
        f"Good luck!"
    )
    await message.reply(answer)


def register_all_handlers(dispatcher):
    dispatcher.register_message_handler(send_welcome, commands=["start"])
    dispatcher.register_message_handler(send_help, commands=["help"])
    dispatcher.register_message_handler(echo)
