import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from index import print_columns

S_KEY = '6509438376:AAGSd-5pyyVl2PTbCOhlDn7KW-R6j2Dhwh0'

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=S_KEY)
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

'''
@dp.message(Command("stat"))
async def cmd_stat(message: types.Message):
'''


@dp.message(Command("col"))
async def cmd_col(message: types.Message):
    all = print_columns()
    for row in all:
        await message.answer(row)


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())