from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.models import DBase
from bot.middleware import handle_file, transcript

db = DBase()


# States
class Form(StatesGroup):
    username = State()  # Will be represented in storage as 'Form:username'


async def subscribe_welcome(message: Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.username.set()
    await message.reply(
        f"Awesome! 🍊\nWhat's repo owner username?\n" f"Type /cancel for break!"
    )


async def cancel_handler(message: Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    # Cancel state and inform user about it
    await state.finish()
    await message.reply("Cancelled!")


async def process_username(message: Message, state: FSMContext):
    """
    Process username
    """
    async with state.proxy() as data:
        data["autor_username"] = message.text

    await state.finish()
    await message.reply(f"You have been subscribe to {data.as_dict()}")


async def echo(message: Message):
    """
    Simple echo handler
    """
    await message.answer(message.text)


async def voicy(message: Message):
    voice = await message.voice.get_file()
    path = "./files/voices"
    file_name = f"{voice.file_id}.ogg"

    await handle_file(message=message, file=voice, file_name=file_name, path=path)
    result = await transcript(f"{path}/{file_name}")
    await message.answer(result)


async def send_welcome(message: Message, db=db):
    """
    This handler will be called when user sends `/start` command
    """
    db.add_user(**message.from_user.values)
    await message.reply(
        f"Hi!\nI'm OrangeBot! 🍊\n"
        f"Now you can subscribe to updates of Github users 🙌\n"
        f"Send /help for more 🍊"
    )


async def send_help(message: Message):
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


def register_all_handlers(dp: Dispatcher):
    dp.register_message_handler(subscribe_welcome, commands=["subscribe"])
    dp.register_message_handler(voicy, content_types=["voice"])
    dp.register_message_handler(cancel_handler, state="*", commands=["cancel"])
    dp.register_message_handler(process_username, state=Form.username)
    dp.register_message_handler(send_welcome, commands=["start"])
    dp.register_message_handler(send_help, commands=["help"])
    dp.register_message_handler(echo)
