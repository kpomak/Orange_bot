from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def unsubscribe_keyboard(db, **kwargs):
    authors = db.get_authors_list(**kwargs)
    buttons = [KeyboardButton(author) for author in authors]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        row_width=1,
    )
    return keyboard
