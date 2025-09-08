import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command

from keyboard import (
    start_keyboard, get_format_keyboard, save_request,
    custom_text_size, custom_image_size, custom_page_split
)
from generation import generate_file
from dotenv import load_dotenv

load_dotenv()  # .env fayldan o‘qiydi
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# User data: vaqtinchalik matn va rasmlar
user_data = {}
user_mode = {}  # auto / custom
user_settings = {}  # custom sozlamalar

# papkalar
os.makedirs("images", exist_ok=True)
os.makedirs("results", exist_ok=True)


@dp.message(Command("start"))
async def start(message: Message):
    user_data[message.from_user.id] = []
    user_mode[message.from_user.id] = "auto"
    user_settings[message.from_user.id] = {}
    await message.answer(
        f"👋 Salom! {message.from_user.first_name}\n\n"
        "Avtomatik yoki Maxsus rejimni tanlang:\n"
        "Avtomatik rejimda o'lchamni Bot o'zi tanlab qilib beradi\n"
        "Maxsus rejimda O'lchamlarni o'zingiz tanlab chiqasiz!",
        reply_markup=start_keyboard()
    )


# "🏁 Tugatish" handler
@dp.callback_query(F.data == "finish")
async def finish(callback: CallbackQuery):
    await callback.message.answer("Qaysi formatda saqlamoqchisiz?", reply_markup=get_format_keyboard())


@dp.callback_query(F.data.startswith("mode_"))
async def choose_mode(callback: CallbackQuery):
    uid = callback.from_user.id
    if callback.data == "mode_auto":
        user_mode[uid] = "auto"
        await callback.message.answer("✅ Avtomatik rejim tanlandi.\nMenga matn yoki rasm yuboring.")
    else:
        user_mode[uid] = "custom"
        await callback.message.answer("📏 Matn o‘lchamini tanlang:", reply_markup=custom_text_size())


@dp.callback_query(F.data.startswith("text_"))
async def set_text_size(callback: CallbackQuery):
    uid = callback.from_user.id
    size = int(callback.data.split("_")[1])
    user_settings[uid]["text_size"] = size
    await callback.message.answer("🖼️ Rasm o‘lchamini tanlang:", reply_markup=custom_image_size())


@dp.callback_query(F.data.startswith("img_"))
async def set_img_size(callback: CallbackQuery):
    uid = callback.from_user.id
    size = callback.data.split("_")[1]
    user_settings[uid]["image_size"] = size
    await callback.message.answer("📄 Necha element bir varoqqa tushsin?", reply_markup=custom_page_split())


@dp.callback_query(F.data.startswith("page_"))
async def set_page_split(callback: CallbackQuery):
    uid = callback.from_user.id
    per_page = int(callback.data.split("_")[1])
    user_settings[uid]["per_page"] = per_page
    await callback.message.answer("✅ Custom sozlamalar saqlandi!\nEndi menga matn yoki rasm yuboring.")


# Matn / rasm yig‘ish
@dp.message(F.photo | F.text)
async def collect(message: Message):
    uid = message.from_user.id
    if uid not in user_data:
        user_data[uid] = []

    if message.photo:
        file_id = message.photo[-1].file_id
        file = await bot.get_file(file_id)
        path = f"images/{uid}_{len(user_data[uid])}.jpg"
        await bot.download_file(file.file_path, path)

        caption = message.caption if message.caption else ""
        user_data[uid].append(("image", path, caption))
        await message.answer("✅ Rasm qo‘shildi", reply_markup=save_request())
    elif message.text:
        user_data[uid].append(("text", message.text))
        await message.answer("✅ Matn qo‘shildi", reply_markup=save_request())


# Callback → file yaratish
@dp.callback_query(F.data.startswith("save_"))
async def save_file(callback: CallbackQuery):
    uid = callback.from_user.id
    if uid not in user_data or not user_data[uid]:
        await callback.message.answer("❌ Hech narsa topilmadi.")
        return

    fmt = callback.data.split("_")[1]
    settings = user_settings[uid] if user_mode[uid] == "custom" else None
    filename = generate_file(fmt, uid, user_data[uid], settings)

    document = FSInputFile(filename)
    await callback.message.answer_document(document)

    # fayllarni o‘chirish
    os.remove(filename)
    for item in user_data[uid]:
        if item[0] == "image" and os.path.exists(item[1]):
            os.remove(item[1])

    user_data[uid] = []


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
