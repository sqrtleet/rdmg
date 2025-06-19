# ---- Сборка фронтенда ----
FROM node:18-alpine AS frontend-builder
WORKDIR /app/client

# Сначала копируем package.json и package-lock.json для кэша npm install
COPY app/client/package*.json ./
RUN npm ci

# Копируем весь код клиента и собираем
COPY app/client/ .
RUN npm run build   # результат в app/client/dist

# ---- Сборка бэкенда ----
FROM python:3.11-slim

# Устанавливаем зависимости системы (если нужны libjpeg, ... — добавьте сюда)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем зависимости Python
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код FastAPI
COPY app/ .

# Экспонируем порт
EXPOSE 8000

# Запуск Uvicorn
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
