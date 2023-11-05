import bcrypt
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
#from Services.test_connection import print_columns
from Services.config_DB import init_config
from Services.config_DB import add_user
from Services.config_DB import get_user, get_user_by_id
from Models.user_models import User
from Services.sys_status import start_thread, stop_thread, create_image
from Services import Auth as auth
from aiogram.types import FSInputFile
from time import sleep

S_KEY = '6509438376:AAGSd-5pyyVl2PTbCOhlDn7KW-R6j2Dhwh0'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=S_KEY)
dp = Dispatcher()

text_not_access = "Команды не найдена!"

def check_access(message):
    return auth.check_session_by_id(message.from_user.id)


# Хэндлер на команду /start
@dp.message(Command("start"))
async def start(message: types.Message):
   await message.answer("Введите /help чтобы увидеть список доступных команд.", reply_markup = markup)


@dp.message(Command("help"))
async def help(message: types.Message):
    if not check_access(message):
        await message.answer("/sign_in login password - чтобы войти!")
        return
    await message.answer("/help - помощь\n/system - посмотреть информацию о состоянии системы\nlisten - подписаться на сообщения о состоянии (доделать!)", reply_markup=markup)

@dp.message(Command("system"))
async def system(message: types.Message):
    if not check_access(message): 
        await message.answer(text_not_access)
        return
    create_image()
    system = FSInputFile('system.png')
    await bot.send_photo(message.from_user.id, system)

@dp.message(Command("add_user"))
async def system(message: types.Message):
    if not check_access(message): 
        await message.answer(text_not_access)
        return
    data = message.text.split(" ")
    if len(data) >= 3:
        if add_user(
            User(name = data[1] , password = auth.get_hash(data[2]), email =None, phonenumber = None, telegrm_id = message.from_user.id)
        ):
            await message.answer("Completed!")
        else:
            await message.answer("user has been yet!")

    else:
        await message.answer("Неверный синтаксис команды")

@dp.message(Command("sign_in"))
async def cmd_col(message: types.Message):
    if check_access(message):
        await message.answer(text_not_access)
        return
    lines = message.text.split(" ")
    if len(lines) >= 3:
        if (auth.check_session(lines[1], lines[2], message.from_user.id)):
            await message.answer("Вход выполнен")
            return
        await message.answer("Неверный логин или пароль!")
        return
    await message.answer("Команда некорректна")

@dp.message(Command("log_out"))
async def log_out(message):
    if (check_access(message)):
        if (auth.break_session(message.from_user.id)):
            await message.answer("Вы вышли!")
    else:
        await message.answer(text_not_access)

@dp.message(Command("buttons"))
async def log_out(message):
    if (check_access(message)):
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text = "Кнопка 1", callback_data="button1")
        keyboard.button(text = "Кнопка 2", callback_data="button2")
        
        await message.answer("Выберите действие:", reply_markup=keyboard.as_markup())
    else:
        await message.answer(text_not_access)

@dp.callback_query()
async def process_callback_data(callback_query: types.CallbackQuery):
    # Здесь вы можете обработать callback_data, например, получить его и сделать что-то с ним
    callback_data = callback_query.data
    # print(callback_data)
    answer = ""
    match callback_data:
        case "button1":
            answer = "Вы нажади на кнопку 1!"
        case "button2":
            answer = "Вы нажади на кнопку 2!"
        case _:
            answer = "Неизвестная кнопка"

    # await callback_query.answer(text=answer) # Клевая фича
    await bot.send_message(callback_query.from_user.id, answer)

listening = False
listeners = set()

@dp.message(Command("listen"))
async def listen(message: types.Message):
    if check_access(message):
        listeners.add(message.from_user.id)
        print(listeners)
        listening = True
        if len(listeners) == 0:
            listening=False
        # тут надо проверить как дела и отправит ответ
        # С помощью этого кусочка можно подписаться на бота 
        # когда что-то слоаматется таким образом всех оповестить

        # if что-то сломалось, то:
        while listening:
            for _id in listeners:
                await bot.send_message(_id, "Privet")
    else:
        await message.answer(text_not_access)


# @dp.message(Command("stat_db"))
# async def cmd_col(message: types.Message):
#     all = print_columns()
#     for row in all:
#         await message.answer(row, reply_markup=markup)

async def main():
    init_config()
    # bob = User(name ="bob", password = ,email =None,phonenumber = None, telegrm_id = None)
    # add_user(bob)
    await dp.start_polling(bot)


kb = [
        [types.KeyboardButton(text="/help")],
        [types.KeyboardButton(text="/system")],
        [types.KeyboardButton(text="/listen")]
    ]
markup = types.ReplyKeyboardMarkup(keyboard=kb)



if __name__ == "__main__":
    start_thread()
    asyncio.run(main())
