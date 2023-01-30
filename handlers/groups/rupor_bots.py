import asyncio
import datetime
import subprocess
import sys

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ContentTypes, CallbackQuery

from keyboards.default import menu_start
from keyboards.inline.in_menu import in_menu_start, in_menu_back, in_menu_back_and_send

from loader import dp, PAYMENTS_PROVIDER_TOKEN, bot
from utils.db_api.db import BotDB



@dp.callback_query_handler(lambda c: c.data.startswith('rupor'))
async def add_channel(call: CallbackQuery, state: FSMContext):
    keyboard = await in_menu_back()

    await call.message.edit_text(text='⚡️Напишите сообщение, что бы '
                                      'оповестить всех администраторов',reply_markup=keyboard)
    await state.set_state('rupor')


@dp.message_handler(state='rupor')
async def start(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.update_data(entities=message.entities)
    await bot.send_message(chat_id=message.from_user.id, text=message.text, entities=message.entities)

    keyboard = await in_menu_back_and_send()

    await message.answer('Рассылаем сообщение?😏',reply_markup=keyboard)

async def send_mess_in_query(userid, text, entities):
    await bot.send_message(chat_id=userid, text=text, entities=entities)



@dp.callback_query_handler(lambda c: c.data.startswith('go_send'),state='*')
async def add_channel(call: CallbackQuery, state: FSMContext):
    get_db_telegram = BotDB()
    users_array = [i['userid'] for i in get_db_telegram.get_all_users_token()]


    data = await state.get_data()
    text = data['text']
    entities = data['entities']
    tasks_send_mess = []
    for __user in users_array:
        tasks_send_mess.append(
            asyncio.create_task(
                send_mess_in_query(
                    userid=__user,
                    text=text,
                    entities=entities
                )))
    send_len = len(await asyncio.gather(*tasks_send_mess))
    keyboard = await in_menu_back()
    await call.message.edit_text(text=f'⚡️Все сообщения отправлены!\n'
                                      f'Отправленно: {send_len}', reply_markup=keyboard)
    await state.finish()


