# Barter Platform 🏷️↔️🏷️  
Монолитное Django‑приложение для обмена вещами («бартер»).  
В репо уже лежат готовые Docker‑файлы и базовая конфигурация PostgreSQL.

---

## Содержание

1. [Стек](#стек)  
2. [Быстрый старт с Docker](#быстрый-старт-с-docker)  
3. [Переменные окружения](#переменные-окружения)  
4. [Частые команды](#частые-команды)  
5. [Локальная разработка без Docker (опционально)](#локальная-разработка-без-docker)  
6. [Тесты](#тесты)  
7. [Автодокументация API](#автодокументация-api)

---

## Стек

| Уровень          | Выбор                               |
|------------------|-------------------------------------|
| Язык             | Python 3.12                         |
| Фреймворк        | Django 4 + Django Templates + Jinja |
| REST API         | Django REST Framework               |
| База данных      | PostgreSQL 16 (alpine)              |
| Контейнеризация  | Docker / docker‑compose v3.9        |
| WSGI‑сервер      | Gunicorn                            |
| Документация API | drf‑spectacular → Swagger / ReDoc   |
| Тесты            | pytest + pytest‑django              |

---

## Быстрый старт с Docker

```bash
# 1. Клонируем репозиторий
git clone https://github.com/A7med373/barter_platform.git
cd barter_platform

# 2. Создаём .env из примера и редактируем при необходимости
cp .env.example .env

# 3. Собираем и запускаем проект
docker compose build
docker compose up -d           # «-d» — в фоне

# 4. Создаём суперпользователя (один раз)
docker compose exec web python manage.py createsuperuser