# 1) Стадия сборки фронтенда (Vue)
FROM node:18-alpine AS frontend-builder
WORKDIR /srv/client

COPY app/client/package*.json ./
RUN npm ci

COPY app/client/ .
RUN npm run build

# 2) Стадия сборки бэкенда (FastAPI)
FROM python:3.11-slim

# если нужны какие-то системные либы, добавьте их тут
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /srv

# Копируем весь код проекта, сохранив структуру
COPY . .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r app/requirements.txt

EXPOSE 8000

# Запускаем Uvicorn по модулю main.py в корне /srv
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
