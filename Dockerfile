FROM node:18-alpine AS frontend-builder
WORKDIR /srv/client

COPY app/client/package*.json ./
RUN npm ci

COPY app/client/ .
RUN npm run build

FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /srv

COPY . .

RUN pip install --no-cache-dir -r app/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"]
