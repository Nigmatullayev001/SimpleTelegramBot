import asyncio
import os
import time
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

load_dotenv()
TOKEN = os.getenv("TOKEN")
RAILWAY_URL = os.getenv("RAILWAY_URL")
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Ma'lumotlar
user_data = {}
files_created = []  # [(filename, timestamp), ...]

os.makedirs("results", exist_ok=True)


# 🧠 START komandasi
@dp.message(Command("start"))
async def start(message: types.Message):
    uid = message.from_user.id
    user_data[uid] = user_data.get(uid, {"count": 0})
    user_data[uid]["count"] += 1

    await message.answer(
        "👋 Salom! Siz botga kirdingiz.\n"
        "Har safar yangi fayl yaratsangiz, u `results/` papkaga saqlanadi."
    )


# 📄 Fayl yaratish
@dp.message(Command("create"))
async def create_file(message: types.Message):
    uid = message.from_user.id
    filename = f"results/{uid}_{int(time.time())}.txt"
    with open(filename, "w") as f:
        f.write(f"File for user {uid}\nCreated: {time.ctime()}")
    files_created.append((filename, time.time()))
    await message.answer(f"✅ Fayl yaratildi: `{filename}`", parse_mode="Markdown")


# ⚙️ ADMIN PANEL
@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("🚫 Siz admin emassiz!")

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="👥 Foydalanuvchilar")],
            [types.KeyboardButton(text="🗂 So‘nggi 5 fayl")],
            [types.KeyboardButton(text="🧹 Fayllarni tozalash")],
        ],
        resize_keyboard=True
    )
    await message.answer("🔐 Admin panel:", reply_markup=keyboard)


# 👥 Foydalanuvchilarni ko‘rish
@dp.message(lambda m: m.text == "👥 Foydalanuvchilar")
async def show_users(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    if not user_data:
        return await message.answer("⚠️ Hozircha foydalanuvchilar yo‘q.")
    text = "👥 Foydalanuvchilar:\n"
    for uid, data in user_data.items():
        text += f"- ID: {uid}, files: {data['count']}\n"
    await message.answer(text)


# 🗂 So‘nggi 5 fayl
@dp.message(lambda m: m.text == "🗂 So‘nggi 5 fayl")
async def last_files(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    if not files_created:
        return await message.answer("⚠️ Fayllar yo‘q.")
    last5 = files_created[-5:]
    text = "🗂 So‘nggi 5 fayl:\n"
    for name, ts in last5:
        text += f"- {name} ({time.ctime(ts)})\n"
    await message.answer(text)


# 🧹 Fayllarni tozalash
@dp.message(lambda m: m.text == "🧹 Fayllarni tozalash")
async def clear_files(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    deleted = 0
    for f, _ in files_created.copy():
        if os.path.exists(f):
            os.remove(f)
            deleted += 1
    files_created.clear()
    await message.answer(f"🧹 {deleted} ta fayl o‘chirildi!")


# ♻️ Avtomatik fayl tozalash
async def auto_clean_files():
    while True:
        now = time.time()
        for f, ts in files_created.copy():
            if now - ts > 600:  # 10 daqiqa = 600 sekund
                if os.path.exists(f):
                    os.remove(f)
                    print(f"🧹 Avto-tozalandi: {f}")
                    files_created.remove((f, ts))
        await asyncio.sleep(60)


# 🌐 Webhook server
def main():
    app = web.Application()
    webhook_path = f"/webhook/{TOKEN}"

    SimpleRequestHandler(dp, bot).register(app, path=webhook_path)
    setup_application(app, dp, bot=bot)

    async def on_startup(app):
        await bot.set_webhook(f"{RAILWAY_URL}{webhook_path}")
        print("✅ Webhook o‘rnatildi!")

        asyncio.create_task(auto_clean_files())

    app.on_startup.append(on_startup)
    return app


if __name__ == "__main__":
    web.run_app(main(), host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
