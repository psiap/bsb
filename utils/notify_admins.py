import logging
import os
import signal
import subprocess
import requests
from aiogram import Dispatcher

from data.config import ADMINS
from utils.db_api.db import BotDB


async def on_startup_notify(dp: Dispatcher):
    get_db_telegram = BotDB()
    all_bots = get_db_telegram.get_all_bots()
    for i in all_bots:
        try:
            os.kill(i["pid"], signal.SIGTERM)
        except:
            pass
        proc = subprocess.Popen(['python', "bots/bot_subs/app.py", f'{i["apitoken"]}', f'{i["userid"]}'],
                                shell=False)
        get_db_telegram.edit_pid_bot(apitoken=i["apitoken"], pid=proc.pid)
        print(i)

    print('Боты запущенны')

    for admin in ADMINS:
        try:
            #await dp.bot.send_message(admin, "Бот Запущен")
            pass
        except Exception as err:
            logging.exception(err)
