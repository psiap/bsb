import asyncio
import csv
import datetime
import itertools
import os
import time

from aiogram import types
from aiogram.dispatcher import FSMContext


from data.config import ADMINS

from loader import dp, bot
from utils.db_api.db import BotDB


@dp.message_handler(text='/admin',state='*')
async def f_search_f(message: types.Message, state: FSMContext):
    __userid = message.from_user.id
    if f"{__userid}" in ADMINS:
        await message.answer(f"Добрый день администратор")
        get_db_telegram = BotDB()
        state_save = f""
        for _point in get_db_telegram.get_full_breakpoint():
            if _point['status'] == "False":
                string_s = f"Номер обращения: <b>{_point['keyid']}</b>\n" \
                           f"Дата обращения: {_point['date_register']}\n" \
                           f"Текст обращения: {_point['text']}\n" \
                           f"---------------------\n\n"
                state_save += string_s

        await message.answer(f"{state_save} Укажите 'Номер обращения'")
        await state.set_state('admin_answer')
