# Базовый образ Python
FROM python:3.12-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Экспонируем порт
EXPOSE 8000

# Разрешаем все хосты для разработки
ENV DJANGO_ALLOWED_HOSTS='*'

# Команда запуска: миграции + статика + Gunicorn
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn onlineShop.wsgi:application --bind 0.0.0.0:8000"]