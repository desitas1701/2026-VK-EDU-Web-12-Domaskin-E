# 2026-VK-EDU-Web-12-Domaskin-E

## Подготовка

1. Создайте локальный файл окружения:

```bash
cp .env.example .env
```

2. При необходимости отредактируйте значения в `.env`.
3. Установите зависимости для компиляции SCSS:

```bash
npm ci
```

## Локальный запуск

В двух терминалах:

```bash
# Терминал 1: автокомпиляция SCSS -> CSS
npm run dev
```

```bash
# Терминал 2: Django
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Команда `runserver` берёт порт из `PORT` в `.env` (по умолчанию `8000`).

## Запуск через Docker Compose

```bash
docker compose up --build
```

Приложение будет доступно на `http://localhost:${PORT:-8000}`.

`docker-compose` запускает два сервиса:
- `web` — Django;
- `scss` — watcher для автокомпиляции `static/scss` в `static/css`.
