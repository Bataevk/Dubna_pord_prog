import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from index import print_columns

S_KEY = '6509438376:AAGSd-5pyyVl2PTbCOhlDn7KW-R6j2Dhwh0'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=S_KEY)
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello! \n This bot represents the state of the pg_stat_activity database - /stat_db ")


@dp.message(Command("stat_db"))
async def cmd_col(message: types.Message):
    all = print_columns()
    for row in all:
        await message.answer(row)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())