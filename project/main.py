import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
#from Services.test_connection import print_columns
from Services.config_DB import init_config, DbConnection
from Services.config_DB import add_user, get_dbconnection, get_user_by_id
from Models.user_models import User
from Services.sys_status import start_thread, stop_thread, create_image
from Services import Auth as auth
from aiogram.types import FSInputFile
from time import sleep
from aiogram.utils.keyboard import InlineKeyboardBuilder
from Services.analyzer import Analizyr

S_KEY = '6509438376:AAGSd-5pyyVl2PTbCOhlDn7KW-R6j2Dhwh0'
markup = None 
logging.basicConfig(level=logging.INFO)
bot = Bot(token=S_KEY)
dp = Dispatcher()

analyzers = {}

text_not_access = "Команды не найдена!"

def check_access(id):
    return auth.check_session_by_id(id)


# Хэндлер на команду /start
@dp.message(Command("start"))
async def start(message: types.Message):
   global markup
   await message.answer("Введите /help чтобы увидеть список доступных команд.", reply_markup = markup)


@dp.message(Command("help"))
async def help(message: types.Message):
    if not check_access(message.from_user.id):
        await message.answer("/sign_in login password - чтобы войти!")
        return
    await message.answer("/help - помощь\n/system - посмотреть информацию о состоянии системы\n/show_my_db - все базы данных\n/show_server_statistic_db - статистика по серверу бд\n/log_out - выйти\n/add_user login password", reply_markup=markup)

@dp.message(Command("system"))
async def system(message: types.Message):
    if not check_access(message.from_user.id): 
        await message.answer(text_not_access)
        return
    create_image()
    system = FSInputFile('system.png')
    await bot.send_photo(message.from_user.id, system)

@dp.message(Command("add_user"))
async def system(message: types.Message):
    if not check_access(message.from_user.id): 
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
    if check_access(message.from_user.id):
        await message.answer(text_not_access)
        return
    lines = message.text.split(" ")
    if len(lines) >= 3:
        if (auth.check_session(lines[1], lines[2], message.from_user.id)):
            await message.answer("Вход выполнен")
            global analyzer1
            conn = get_dbconnection(
                1
            )
            #Словарь аналзаторов, по id из телеграмма
            #Хост, Порт, имяпользователя, пароль
            analyzers[message.from_user.id] = Analizyr('localhost', '5432', 'postgres', '123451515') 
            return 
        await message.answer("Неверный логин или пароль!")
        return
    await message.answer("Команда некорректна")

@dp.message(Command("log_out"))
async def log_out(message):
    if (check_access(message.from_user.id)):
        if (auth.break_session(message.from_user.id)):
            await message.answer("Вы вышли!")
    else:
        await message.answer(text_not_access)

@dp.message(Command("show_my_db"))
async def log_out(message):
    if (check_access(message.from_user.id)):
        if message.from_user.id in analyzers:
            response = analyzers[message.from_user.id].get_data_name_into()

            #datid | datname | pid | usename | wait_event_type | wait_event | state
            keyboard = InlineKeyboardBuilder()
            anw = "Мои базы данных:\ndatname | pid | state\n"
            for item in response:
                anw += f"{item[1]} {item[2]} {item[6]}\n"
                keyboard.button(text = str(item[1]) + " " + str(item[2]), callback_data=f"db {item[2]}")

            keyboard.adjust(1)
            await message.answer(anw, reply_markup=keyboard.as_markup())
        else:
            await message.answer("Базы данных отсутствуют")
    else:
        await message.answer(text_not_access)


@dp.message(Command("show_server_statistic_db"))
async def log_out(message):
    if (check_access(message.from_user.id)):
        if message.from_user.id in analyzers:
            anw = "1) Время начала активных сессий\n2) Кол-во активных сессий\n3) Состояния сессий"
            
            keyboard = InlineKeyboardBuilder()

            keyboard.button(text = "1", callback_data=f"time_ls")
            keyboard.button(text = "2", callback_data=f"cnt_ls")
            keyboard.button(text = "3", callback_data=f"event_ls")

            keyboard.adjust(3)
            await message.answer(anw, reply_markup=keyboard.as_markup())
        else:
            await message.answer("Базы данных отсутствуют")
    else:
        await message.answer(text_not_access)


@dp.callback_query()
async def process_callback_data(callback_query: types.CallbackQuery):
    # Здесь вы можете обработать callback_data, например, получить его и сделать что-то с ним
    callback_data = callback_query.data
    if not check_access(callback_query.from_user.id): callback_data = ""
    # print(callback_data)
    answer = ""
    builder = None
    match callback_data:
        case "time_ls":
            res = analyzers[callback_query.from_user.id].get_long_session()
            answer = "datid | datname | pid | backend_start\n" 
            for item in res:
                answer += f"{item[0]} \t{item[1]} \t{item[2]} \t{item[3]}\n"
        case "cnt_ls":
            res = analyzers[callback_query.from_user.id].get_cnt_session()
            answer = "datid | datname | numbackends\n"  
            for item in res:
                answer += f"{item[0]} \t{item[1]} \t{item[2]}\n"
        case "event_ls":
            res = analyzers[callback_query.from_user.id].get_stat_session()
            answer = "datid | datname | pid | w_evnt_tp\n" 
            for item in res:
                answer += f"{item[0]} \t{item[1]} \t{item[2]} \t{item[3]}\n"
        case _:
            command = callback_data.split(" ")
            if len(command) > 1:
                pid = command[1]
                match command[0]:
                    case "db":
                        keyboard = InlineKeyboardBuilder()
                        
                        keyboard.button(text = "del procces", callback_data=f"delp {pid}")
                        keyboard.button(text = "del session", callback_data=f"dels {pid}")
                        
                        keyboard.adjust(1)
                        answer = analyzers[callback_query.from_user.id].prnt_all_stat_activity(pid)
                        builder = keyboard.as_markup()
                    
                    case "dels":
                        #pid 
                        an = analyzers[callback_query.from_user.id].delete_session(pid)
                        answer = "Completed"
                    case "delp":
                        #pid
                        an = analyzers[callback_query.from_user.id].delete_procces(pid)
                        answer = "Completed"

            else:
                answer = "Неизвестная кнопка"

    # await callback_query.answer(text=answer) # Клевая фича
    await bot.send_message(callback_query.from_user.id, answer, reply_markup=builder)

listening = False
listeners = set()

'''
@dp.message(Command("listen"))
async def listen(message: types.Message):
    if check_access(message.from_user.id):
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
'''

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
        [types.KeyboardButton(text="/show_my_db")]
    ]
markup = types.ReplyKeyboardMarkup(keyboard=kb)



if __name__ == "__main__":
    start_thread()
    asyncio.run(main())
