import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from data.captcha import Captcha
from keyboards.default import menu_start
from keyboards.inline.in_menu import in_menu_start
from loader import dp, bot
from utils.db_api.db import BotDB


async def anti_flood(*args, **kwargs):
    message = args[0]
    if message.from_user.id not in Captcha.passed_captcha_users:
        captcha = Captcha()
        captcha.register_handlers(dp)

        await bot.send_message(
            message.chat.id,
            captcha.get_caption(),
            reply_markup=captcha.get_captcha_keyboard()
        )
        return

@dp.message_handler(text='🔙 Назад', state='*')
async def back(message: types.Message, state: FSMContext):
    await message.answer("", reply_markup=menu_start)
    await state.finish()


@dp.message_handler(CommandStart(),state='*')
@dp.throttled(anti_flood,rate=3)
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    users_id = message.from_user.id
    keyboard = await in_menu_start(users_id)

    await state.finish()
    await message.answer("<i>Здравствуйте 👋</i>\n\n"
                         "<i>В</i> <b>Brotherhood Concierge</b> <i>вы можете принимать заявки ваших подписчиков, отправить "
                         "вступившим подписчикам приветственное сообщение, "
                         "а так же отправить прощальное сообщение при отписке от вас😎</i>\n\n"
                         "<i>Так же доступна выгрузка вашей накопившейся базы данных и добавление выгруженой базы данных для рассылки☝️</i>\n\n"
                         "<b>⚠️Внимание!</b> Бот работает в Канале/Группе/Чате, для добавления в Группу/Чат посмотрите гайд👉 <a href='https://telegra.ph/Dobavlenie-GruppyCHata-v-Brotherhood-Concierge-11-25'><b>ТЫК</b></a>", reply_markup=keyboard, disable_web_page_preview=True)
