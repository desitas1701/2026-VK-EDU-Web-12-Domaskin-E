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

## Роуты

| URL | Метод | Описание | Параметры пути | GET-параметры |
| --- | --- | --- | --- | --- |
| `/` | GET | Главная, редирект на список вопросов | - | `as_user` |
| `/questions/` | GET | Редирект на новые вопросы | - | `as_user` |
| `/questions/newest/` | GET | Новые вопросы | - | `page`, `as_user` |
| `/questions/hottest/` | GET | Горячие вопросы (по голосам) | - | `page`, `as_user` |
| `/questions/ask/` | GET | Страница создания вопроса | - | `as_user` |
| `/questions/<id>/` | GET | Страница вопроса и его ответов | `id: int` | `as_user` |
| `/questions/<id>/edit/` | GET | Страница редактирования вопроса | `id: int` | `as_user` |
| `/questions/<id>/delete/` | GET | Удаление вопроса (сейчас редирект на главную) | `id: int` | `as_user` |
| `/answers/<id>/edit/` | GET | Страница редактирования ответа | `id: int` | `as_user` |
| `/search/` | GET | Поиск вопросов | - | `q`, `page`, `as_user` |
| `/tags/` | GET | Редирект на главную | - | `as_user` |
| `/tags/<tag>/` | GET | Вопросы по тегу | `tag: slug` | `page`, `as_user` |
| `/users/` | GET | Список пользователей | - | `page`, `as_user` |
| `/users/<id>/` | GET | Профиль пользователя и его вопросы | `id: int` | `page`, `as_user` |
| `/users/login/` | GET | Страница входа | - | `as_user` |
| `/users/logout/` | GET | Выход (сейчас редирект на главную) | - | `as_user` |
| `/users/settings/` | GET | Настройки профиля | - | `as_user` |
| `/users/signup/` | GET | Регистрация | - | `as_user` |

## Эмуляция пользователя через `as_user`

В любой GET-запрос можно добавить `as_user=<user_id>`, и интерфейс будет отображаться от имени этого пользователя.

Примеры:
- `/questions/newest/?as_user=5`
- `/search/?q=django&as_user=12`
- `/users/7/?page=2&as_user=7`

Поведение по текущему коду:
- параметр читается в `AuthenticationEmulatorMiddleware` и сохраняется в `request.session['user_id']`;
- если `as_user` не передавать, остаётся последнее значение из сессии;
- если передано нечисловое значение (`as_user=abc`), используется `0` (гость);
- если `user_id` вне диапазона тестовых пользователей, показывается гость;
- валидные `user_id` сейчас: `1..100` (генератор тестовых данных).
