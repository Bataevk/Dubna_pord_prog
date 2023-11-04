import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
#from Services.test_connection import print_columns
from Services.config_DB import init_config
from Services.config_DB import add_user
from Services.config_DB import get_user
from Models.user_models import User
from Services.sys_status import start_thread, stop_thread, create_image
from Services.check_db_status import is_fine
from Services import Auth as auth
from aiogram.types import FSInputFile
from time import sleep

S_KEY = '6509438376:AAGSd-5pyyVl2PTbCOhlDn7KW-R6j2Dhwh0'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=S_KEY)
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def start(message: types.Message):
   await message.answer("Введите /help чтобы увидеть список доступных команд.", reply_markup = markup)


@dp.message(Command("help"))
async def help(message: types.Message):
    await message.answer("/help - помощь\n/system - посмотреть информацию о состоянии системы\nlisten - подписаться на сообщения о состоянии (доделать!)", reply_markup=markup)

@dp.message(Command("system"))
async def system(message: types.Message):
    create_image()
    system = FSInputFile('system.png')
    await bot.send_photo(message.from_user.id, system)


@dp.message(Command("sign_in"))
async def cmd_col(message: types.Message):
    lines = message.text.split(" ")
    if len(lines) >= 2:
        if (auth.check_session(lines[1], lines[2])):
            await message.answer("Вход выполнен")
            return
        await message.answer("Неверный логин или пароль!")
        return
    await message.answer("Команда некорректна")




listening = False
listeners = set()

@dp.message(Command("listen"))
async def listen(message: types.Message):
    listeners.add(message.from_user.id)
    print(listeners)

    # тут надо проверить как дела и отправит ответ
    # С помощью этого кусочка можно подписаться на бота 
    # когда что-то слоаматется таким образом всех оповестить
    if is_fine('test') != True:
    # if что-то сломалось, то:
        for _id in listeners:
            await bot.send_message(_id, check('test'))


# @dp.message(Command("stat_db"))
# async def cmd_col(message: types.Message):
#     all = print_columns()
#     for row in all:
#         await message.answer(row, reply_markup=markup)

async def main():
    init_config()
    bob = User(name ="sss", password = "lol",email =None,phonenumber = None, telegrm_id = None)
    bob1 = User(name ="sss1", password = "lol",email =None,phonenumber = None, telegrm_id = None)
    add_user(bob)
    add_user(bob1)
    #print(get_user("sss1").user_connections)
    await dp.start_polling(bot)


kb = [
        [types.KeyboardButton(text="/help")]
        [types.KeyboardButton(text="/system")]
        [types.KeyboardButton(text="/listen")]
    ]
markup = types.ReplyKeyboardMarkup(keyboard=kb)



if __name__ == "__main__":
    start_thread()
    asyncio.run(main())
