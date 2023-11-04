import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
#from Services.test_connection import print_columns
from Services.config_DB import init_config
from Services.config_DB import add_user
from Services.config_DB import get_user
from Models.user_models import User

S_KEY = '6509438376:AAGSd-5pyyVl2PTbCOhlDn7KW-R6j2Dhwh0'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=S_KEY)
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    
    await message.answer("Hello! \n This bot represents the state of the pg_stat_activity database - /stat_db ", reply_markup = markup)


@dp.message(Command("help"))
async def help(message: types.Message):
    await message.answer("/stat_db - вывести всю статистику \n/help - помощь", reply_markup=markup)


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
    print(get_user("sss1","lol").user_connections)
   # await dp.start_polling(bot)


kb = [
        [types.KeyboardButton(text="/stat_db")]
    ]
markup = types.ReplyKeyboardMarkup(keyboard=kb)



if __name__ == "__main__":
    asyncio.run(main())