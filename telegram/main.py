import logging
import asyncio
from aiogram import Bot, Dispatcher, types

API_TOKEN = '6404033562:AAFFUFrDwtt59l9_ON_An2npr2ZnMRr6WQ4'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler()
async def return_message(message: types.Message):
    await message.answer(message.text.upper())


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
