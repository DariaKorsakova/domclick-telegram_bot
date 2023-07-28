import asyncio
from aiogram import Bot, Dispatcher, executor
from config import BOT_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# бот - сервер взмдщ с API telegram
storage = MemoryStorage()
loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN, parse_mode='HTML')  # cоздание бота для форматирования как в html
dp = Dispatcher(bot, loop=loop, storage=storage)  # принимает все апдейты и обрабатывает их


if __name__ == "__main__":
    from handlers import dp, send_to_admin
    executor.start_polling(dp, on_startup=send_to_admin, skip_updates=True)  # Запуск сервер который запускает бота
