# Barter Platform

MVP-платформа для обмена товарами между пользователями. Проект показывает типовой backend-подход для Django-приложения: модели, формы, views, шаблоны, PostgreSQL, Docker, Nginx и тесты.

## Возможности

- Регистрация и аутентификация пользователей.
- Создание, редактирование и удаление объявлений.
- Просмотр объявлений с фильтрацией по категории и состоянию товара.
- Создание предложений обмена между пользователями.
- Просмотр и изменение статуса предложений обмена.
- Загрузка изображений для объявлений.
- Покрытие основной логики тестами.

## Стек

- Python
- Django
- PostgreSQL
- Docker, Docker Compose
- Nginx
- Gunicorn
- Pytest

## Запуск через Docker

Создайте файл `.env` в корне проекта:

```env
POSTGRES_DB=barter
POSTGRES_USER=barter
POSTGRES_PASSWORD=barter
DB_HOST=db
DB_PORT=5432
```

Запустите сервисы:

```bash
docker compose up --build
```

После запуска приложение будет доступно по адресу:

```text
http://localhost
```

## Локальный запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Тесты

```bash
pytest
```

## Структура

```text
apps/accounts/  - пользователи и регистрация
apps/ads/       - объявления и предложения обмена
templates/      - HTML-шаблоны
Dockerfile      - образ backend-приложения
docker-compose.yml
nginx.conf
```

## Что демонстрирует проект

- Разделение Django-приложения на доменные apps.
- Работу с PostgreSQL в Docker-окружении.
- Production-like запуск через Gunicorn и Nginx.
- Тестирование моделей и views.
