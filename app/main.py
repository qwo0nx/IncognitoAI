import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from .config import settings
from .handlers import router
from webapp.server import start_web_server

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)

    # Запускаем веб-сервер (для Mini App)
    await start_web_server()

    @dp.message(Command('app'))
    async def open_app(m: Message):
        # Ссылка будет браться из переменной окружения (Render её подставит)
        import os
        url = os.getenv("WEBAPP_URL", "https://localhost:8080")
        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="🚀 Открыть Agent-Monster", web_app=WebAppInfo(url=url))
        ]])
        await m.answer("Нажми кнопку ниже, чтобы открыть своего ИИ:", reply_markup=kb)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())