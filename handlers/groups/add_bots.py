import asyncio
import datetime
import subprocess
import sys

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ContentTypes, CallbackQuery

from keyboards.default import menu_start
from keyboards.inline.in_menu import in_menu_start

from loader import dp, PAYMENTS_PROVIDER_TOKEN, bot
from utils.db_api.db import BotDB

@dp.callback_query_handler(lambda c: c.data.startswith('sback'),state='*')
async def add_channel(call: CallbackQuery, state: FSMContext):
    users_id = call.from_user.id
    keyboard = await in_menu_start(users_id)

    await state.finish()
    await call.message.edit_text("<b>👋 Привет!</b>\n\n"
                         "Я могу создавать тебе полезного бота🤖 для администрирования ТГ канала бесплатно🆓!", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data.startswith('addbots'))
async def add_channel(call: CallbackQuery, state: FSMContext):
    __userid = call.from_user.id
    path_data_file = call.data.split(' ')[-1]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text=f"🔙 Назад", callback_data=f"sback"))

    await call.message.edit_text(text='Для создания своего бота для администрирования:\n'
                                      '1. Создайте бота в @BotFather\n'
                                      '2. Пришлите мне токен бота.',reply_markup=keyboard)
    await state.set_state('addbots')


@dp.message_handler(state='addbots')
async def start(message: types.Message, state: FSMContext):
    users_id = message.from_user.id
    keyboard = await in_menu_start(users_id)
    proc = subprocess.Popen(['python', "bots/bot_subs/app.py", f'{message.text}',f"{message.from_user.id}"],
                            shell=False)
    msg = await message.answer("Токен получен, мы сейчас его обрабатываем 💤")
    get_db_telegram = BotDB()
    await asyncio.sleep(2)
    if get_db_telegram.check_bots(message.text):
        get_db_telegram.edit_pid_bot(apitoken=message.text, pid=proc.pid)

        bots_temp = get_db_telegram.get_bot_in_api_token(apitoken=message.text)
        await message.answer(f'🛠Бот - @{bots_temp["username"]} запущен и добавлен в ваши боты✅\n'
                             'Удачного использования', reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text=f"🔙 Назад", callback_data=f"sback"))
        await message.answer('♨️Что-то с вашим токеном не так, попробуйте другой',reply_markup=keyboard)
        proc.kill()
    await state.finish()
