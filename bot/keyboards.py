from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def unsubscribe_keyboard(db, **kwargs):
    authors = db.get_authors(**kwargs)
    usernames = [KeyboardButton(author.username) for author in authors]
    keyboard = ReplyKeyboardMarkup(
        keyboard=usernames,
        resize_keyboard=True,
        row_width=1,
    )
    return keyboard
