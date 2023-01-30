from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

menu_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Мои каналы"),
            KeyboardButton(text="Рассылка"),
        ],
    ],
    resize_keyboard=True
)