import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from keyboard import get_template_keyboard
load_dotenv()
TOKEN = os.getenv("TOKEN")
RAILWAY_URL = os.getenv("RAILWAY_URL")

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}
user_template = {}
user_settings = {}

os.makedirs("images", exist_ok=True)
os.makedirs("results", exist_ok=True)


@dp.message(Command("start"))
async def start(message: Message):
    uid = message.from_user.id
    user_data[uid] = []
    user_template[uid] = "green"
    user_settings[uid] = {"text_size": 18, "per_page": 1}

    await message.answer(
        "👋 Salom!\nMenga matn yoki rasm yuboring.\n"
        "Oxirida 🏁 Tugatish tugmasini bosing.\n\n"
        "🎨 Avval dizayn tanlang:",
        reply_markup=get_template_keyboard()
    )


def main():
    app = web.Application()
    webhook_path = f"/webhook/{TOKEN}"

    # Handlersni register qilish
    SimpleRequestHandler(dp, bot).register(app, path=webhook_path)
    setup_application(app, dp, bot=bot)

    # startupda webhook set qilish
    async def on_startup(app):
        await bot.set_webhook(f"{RAILWAY_URL}{webhook_path}")
        print("Webhook set ✅")

    app.on_startup.append(on_startup)
    return app



if __name__ == "__main__":
    web.run_app(main(), host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
