from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext

# from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove

from bot.keyboards import unsubscribe_keyboard
from bot.middleware import handle_file, transcript
from bot.models import DBase
from utils.exceptions import AuthorNotFoundError, UserNotFoundError
from utils.translator import translator

db = DBase()


# States
class SubscribeForm(StatesGroup):
    username = State()  # Will be represented in storage as 'Form:username'


class UnsubscribeForm(StatesGroup):
    username = State()


# Handlers
async def subscribe_welcome(message: Message):
    """
    Conversation entry point
    """
    # Set state
    await SubscribeForm.username.set()
    await message.reply(
        f"Awesome! 🍊\nWhat's repo owners username?\nType /cancel for break!"
    )


async def unsubscribe_welcome(message: Message):
    """
    Conversation entry point
    """
    await UnsubscribeForm.username.set()
    await message.reply(
        f"Awesome! 🍊\nWhich user would you like to unsubscribe from?\n",
        reply_markup=unsubscribe_keyboard(db, **message.from_user.values),
    )


async def process_unsubscribe(message: Message, state: FSMContext):
    """
    Process username
    """
    async with state.proxy() as data:
        data["author_username"] = message.text

    await state.finish()

    try:
        db.unsubscribe_author(**message.from_user.values, **data.as_dict())
    except ValueError:
        await message.reply(
            f"User {message.text} not found 👀", reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.reply(
            f"You have been unsubscribe from {message.text}",
            reply_markup=ReplyKeyboardRemove(),
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
    await message.reply("Cancelled!", reply_markup=ReplyKeyboardRemove())


async def process_subscribe(message: Message, state: FSMContext):
    """
    Process username
    """
    async with state.proxy() as data:
        data["author_username"] = message.text

    await state.finish()

    try:
        db.sudscribe_on_author(**message.from_user.values, **data.as_dict())
    except UserNotFoundError:
        await message.reply(f"You should register first! 🤨\nType /start 🍊")
    except AuthorNotFoundError:
        await message.reply(f"Github user {message.text} not found 👀")
    else:
        await message.reply(f"You have been subscribe to {message.text}")


async def echo(message: Message):
    """
    Simple echo handler
    """
    translation = translator.translate(message.text)
    await message.answer(
        f"```Python\n{translation.text}```",
        parse_mode="MarkdownV2",
        reply_markup=ReplyKeyboardRemove(),
    )


async def voicy(message: Message):
    voice = await message.voice.get_file()
    path = "./files/voices"
    file_name = f"{voice.file_id}.ogg"

    await handle_file(message=message, file=voice, file_name=file_name, path=path)
    result = await transcript(f"{path}/{file_name}")
    if not result:
        result = "I'm sorry! 🍊\nI didn't hear anything! 😔"
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
    dp.register_message_handler(unsubscribe_welcome, commands=["unsubscribe"])
    dp.register_message_handler(voicy, content_types=["voice"])
    dp.register_message_handler(
        cancel_handler,
        state="*",
        commands=["cancel"],
    )
    # dp.register_message_handler(
    #     cancel_handler, Text(equals="cancel", ignore_case=True), state="*"
    # )
    dp.register_message_handler(process_subscribe, state=SubscribeForm.username)
    dp.register_message_handler(process_unsubscribe, state=UnsubscribeForm.username)
    dp.register_message_handler(send_welcome, commands=["start"])
    dp.register_message_handler(send_help, commands=["help"])
    dp.register_message_handler(echo)
