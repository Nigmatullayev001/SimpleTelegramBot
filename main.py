from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

from aiogram.types import InputMediaPhoto

API_TOKEN = "8195800231:AAEvfZYkwOw4RcAxM0FYuhJb16K9WbCoTCM"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

python_img = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYZqZkpMyiN2uSuT7GAf6JSkJ44YsZqoQHdw&s'
cpp_img = 'https://www.vikingsoftware.com/wp-content/uploads/2024/02/C-2.png'
aiogram_img = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlZeLqiLCJLB7mw7-qk1X17C__Qkxq83wWAA&s'


@dp.message(Command("start"))
async def send_start(message: types.Message):
    await message.answer(text="Salom botga xush kelibsiz. dumbul!!")


@dp.message(Command("about"))
async def send_about(message: types.Message):
    await message.answer(text="DUMBULlaR BOTI. dumbul!!")


@dp.message(Command("help"))
async def send_help(message: types.Message):
    await message.answer(text="""/start - botga Start berish
/help - botdan yordam olish
/about - bot haqida ma'lumot olish""")


@dp.message(Command("photo_list"))
async def send_help(message: types.Message):
    media=[
        InputMediaPhoto(media=python_img, caption="Python rasm"),
        InputMediaPhoto(media=cpp_img, caption="C++ rasm"),
        InputMediaPhoto(media=aiogram_img, caption="Aiogram rasm"),
    ]
    await message.bot.send_media_group(chat_id=message.chat.id, media=media)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
