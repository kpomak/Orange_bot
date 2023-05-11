from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.models import DBase

db = DBase()


# States
class Form(StatesGroup):
    username = State()  # Will be represented in storage as 'Form:username'


async def subscribe_welcome(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.username.set()
    await message.reply(
        f"Awesome! 🍊\nWhat's repo owner username?\n" f"Type /cancel for break!"
    )


async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    # Cancel state and inform user about it
    await state.finish()
    await message.reply("Cancelled!")


async def process_username(message: types.Message, state: FSMContext):
    """
    Process username
    """
    async with state.proxy() as data:
        data["autor_username"] = message.text

    await state.finish()
    await message.reply(f"You have been subscribe to {data.as_dict()}")


async def echo(message: types.Message):
    """
    Simple echo handler
    """
    await message.answer(message.text)


async def send_welcome(message: types.Message, db=db):
    """
    This handler will be called when user sends `/start` command
    """
    db.add_user(**message.from_user.values)
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
    dispatcher.register_message_handler(subscribe_welcome, commands=["subscribe"])
    dispatcher.register_message_handler(cancel_handler, state="*", commands=["cancel"])
    dispatcher.register_message_handler(process_username, state=Form.username)
    dispatcher.register_message_handler(send_welcome, commands=["start"])
    dispatcher.register_message_handler(send_help, commands=["help"])
    dispatcher.register_message_handler(echo)
