import logging
import ssl
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties
from aiohttp import web
import asyncio

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Токен бота
API_TOKEN = "8552558705:AAGRGH3W5yH5SWc4UH-b-SN5lmeJlCYsfXM"

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# URL вашего Mini App
MINI_APP_URL = "https://msk1.bot_1765377958_2149_femilianferuk.bothost.ru/"

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = """
<b>👋 Добро пожаловать в Nezeex Store!</b>

✨ <b>Физ</b> — это номер аккаунта, зарегистрированный на реального человека. 
Вся информация выдаётся о нём, а не о вас! ✨

🛒 <b>Все покупки доступны через наш Mini App:</b>

📱 <b>Нажмите кнопку ниже, чтобы открыть магазин</b>
"""
    
    # Создаем кнопку с Mini App
    keyboard = InlineKeyboardBuilder()
    
    # Основная кнопка Mini App
    keyboard.button(
        text="🚀 Открыть магазин",
        web_app=WebAppInfo(url=MINI_APP_URL)
    )
    
    # Дополнительные кнопки
    keyboard.row(
        InlineKeyboardButton(text="👨‍💻 Поддержка", url="https://t.me/v3estnikov"),
        InlineKeyboardButton(text="💬 Отзывы", url="https://t.me/otzuvuvestnikaa")
    )
    
    # Кнопка инструкции
    keyboard.row(
        InlineKeyboardButton(text="❓ Как купить", callback_data="how_to_buy")
    )
    
    await message.answer_photo(
        photo="https://img.freepik.com/free-vector/flat-design-tg-logo-template_23-2149430298.jpg",
        caption=welcome_text,
        reply_markup=keyboard.as_markup()
    )

# Инструкция по покупке
@dp.callback_query(lambda callback: callback.data == "how_to_buy")
async def show_instructions(callback: types.CallbackQuery):
    instructions = """
<b>📋 Как купить аккаунт:</b>

1. <b>Откройте Mini App</b> (кнопка ниже)
2. <b>Выберите страну</b> из списка
3. <b>Выберите опции:</b>
   • 🔥 Прогретый (x1.3)
   • 🛡️ С отлегой (x1.4)
   • 🔥🛡️ Обе опции (x1.7)
4. <b>Оплатите</b> через Crypto Bot
5. <b>Получите данные</b> аккаунта

<b>💳 Оплата:</b> Только в долларах ($) через Crypto Bot
<b>⚡ Доставка:</b> Мгновенно после оплаты
"""
    
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text="🚀 Открыть магазин",
        web_app=WebAppInfo(url=MINI_APP_URL)
    )
    keyboard.button(text="🔙 Назад", callback_data="back_to_main")
    keyboard.adjust(1)
    
    await callback.message.edit_caption(
        caption=instructions,
        reply_markup=keyboard.as_markup()
    )
    await callback.answer()

# Возврат в главное меню
@dp.callback_query(lambda callback: callback.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    welcome_text = """
<b>👋 Добро пожаловать в Nezeex Store!</b>

✨ <b>Физ</b> — это номер аккаунта, зарегистрированный на реального человека. 
Вся информация выдаётся о нём, а не о вас! ✨

🛒 <b>Все покупки доступны через наш Mini App:</b>

📱 <b>Нажмите кнопку ниже, чтобы открыть магазин</b>
"""
    
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text="🚀 Открыть магазин",
        web_app=WebAppInfo(url=MINI_APP_URL)
    )
    keyboard.row(
        InlineKeyboardButton(text="👨‍💻 Поддержка", url="https://t.me/v3estnikov"),
        InlineKeyboardButton(text="💬 Отзывы", url="https://t.me/otzuvuvestnikaa")
    )
    keyboard.row(
        InlineKeyboardButton(text="❓ Как купить", callback_data="how_to_buy")
    )
    
    await callback.message.edit_caption(
        caption=welcome_text,
        reply_markup=keyboard.as_markup()
    )
    await callback.answer()

# Команда /app
@dp.message(Command("app"))
async def cmd_app(message: types.Message):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text="📱 Открыть Mini App",
        web_app=WebAppInfo(url=MINI_APP_URL)
    )
    
    await message.answer(
        "<b>Нажмите кнопку ниже, чтобы открыть магазин:</b>",
        reply_markup=keyboard.as_markup()
    )

# Команда /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = """
<b>❓ Помощь по боту:</b>

<b>Основные команды:</b>
/start - Главное меню
/app - Открыть Mini App
/help - Эта справка

<b>Проблемы с Mini App?</b>
• Проверьте интернет-соединение
• Обновите Telegram до последней версии
• Перезапустите бота (/start)

<b>Техническая поддержка:</b>
• @v3estnikov (основной)
• Время ответа: 5-30 минут

<b>Отзывы покупателей:</b>
• @otzuvuvestnikaa
"""
    
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text="🚀 Открыть магазин",
        web_app=WebAppInfo(url=MINI_APP_URL)
    )
    
    await message.answer(
        help_text,
        reply_markup=keyboard.as_markup()
    )

# Обработка всех текстовых сообщений
@dp.message()
async def handle_all_messages(message: types.Message):
    # Игнорируем служебные сообщения
    if message.via_bot:
        return
    
    # Отвечаем приглашением в Mini App
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text="🚀 Открыть магазин",
        web_app=WebAppInfo(url=MINI_APP_URL)
    )
    
    await message.answer(
        "<b>Для покупки телеграмм аккаунтов откройте наш Mini App:</b>",
        reply_markup=keyboard.as_markup()
    )

# Веб-сервер для Mini App (порт 3000)
async def mini_app_handler(request):
    return web.Response(
        text="Mini App сервер работает!",
        content_type='text/html'
    )

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', mini_app_handler)
    
    # Можно добавить статические файлы для Mini App
    # app.router.add_static('/static/', path='static/')
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 3000)
    await site.start()
    logger.info("Mini App сервер запущен на порту 3000")
    return runner

# Основная функция запуска
async def main():
    logger.info("Запуск бота и Mini App сервера...")
    
    # Запускаем веб-сервер для Mini App
    web_runner = await start_web_server()
    
    try:
        # Запускаем бота
        logger.info("Бот запущен!")
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Остановка бота...")
    finally:
        # Очищаем ресурсы
        await web_runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
