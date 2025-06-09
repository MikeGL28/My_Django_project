FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем содержимое mysite/ внутрь контейнера
COPY mysite/ .

# Запускаем сервер и бота
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000 & python programming/bot_telegram.py"]