import os
import sys
import requests
import django
from pathlib import Path
from django.core.files.base import ContentFile
from asgiref.sync import sync_to_async

# Библиотека aiogram
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import asyncio

# Определяем пути
PROJECT_DIR = Path(__file__).resolve().parent.parent.parent  # MyProject_at_Django/
MYSITE_DIR = Path(__file__).resolve().parent.parent           # mysite/

# Добавляем пути в PYTHONPATH
sys.path.append(str(PROJECT_DIR))
sys.path.append(str(MYSITE_DIR))

# Указываем, где находится settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# Теперь можно инициализировать Django
django.setup()

# Импорт модели
from programming.models import TelegramPost

# Инициализация бота и диспетчера
from programming.config import API_TOKEN, ADMIN_ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ У вас нет доступа к этому боту.")
        return

    await message.answer("Привет! Отправь мне любой текст, и я опубликую его на сайте.")

# Обработка любого текстового сообщения
@dp.message()
async def handle_message(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    # Получаем текст или подпись к фото
    text = message.text or message.caption or ""

    try:
        post = await sync_to_async(TelegramPost.objects.create)(text=text)
        print(f"✅ Пост создан: {post.id} — '{post.text}'")

        if message.photo:
            photo_file = await bot.get_file(message.photo[-1].file_id)
            file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{photo_file.file_path}"

            response = requests.get(file_url)
            if response.status_code == 200:
                image_content = ContentFile(response.content)
                image_name = f"{photo_file.file_unique_id}.jpg"

                await sync_to_async(post.image.save)(image_name, image_content)
                await sync_to_async(post.save)()
                print(f"🖼️ Изображение добавлено к посту {post.id}")

        await message.reply("✅ Сообщение получено и добавлено на сайт!")

    except Exception as e:
        print(f"❌ Ошибка при обработке сообщения: {e}")
        import traceback
        print(traceback.format_exc())

# Запуск бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())