import asyncio
import os
from aiohttp import web
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, FSInputFile


load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    raise ValueError("Переменная BOT_TOKEN не найдена!")

dp = Dispatcher()

router = Router()
my_reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='👤 Моє резюме'), KeyboardButton(text='👨‍💻 Посилання на мій gitHub')],
        [KeyboardButton(text='📞 Звязок зі мною')]
    ],
    resize_keyboard=True,
    input_field_placeholder="Обери дію"
)

async def health_check(request):
    return web.Response(text="Bot is alive!")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Доброго дня вас вітає резюме бот", reply_markup=my_reply_kb)

@dp.message(F.text == "👤 Моє резюме")
async def show_profile(message: types.Message):

    resume_file = FSInputFile('Ризюме.pdf')

    await message.answer_document(
        document=resume_file,
        caption="Доброго дня! Ось моє резюме📄"
    )
@dp.message(F.text == "👨‍💻 Посилання на мій gitHub")
async def show_profile(message: types.Message):

    await message.answer("https://github.com/Nikita-tg-python")

@dp.message(F.text == "📞 Звязок зі мною")
async def show_profile(message: types.Message):

    await message.answer("Номер телефона: +380 68 192 65 18\nТелеграм: @Necro_fus\nПочта: nikitakryvyj@gmail.com")
@dp.message()
async def echo_message(message: types.Message):

    await message.reply(message.text)


async def main():

    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    await site.start()
    print("Фейковый сервер запущен на порту 8000")

    bot = Bot(token=TOKEN)
    
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())