# Barter Platform MVP

### ВАЖНО
Я решил реализовать Docker, nginx, гибрид между монолит и микросервисы.
Мог бы еще реализовать RestAPI, CI\CD и другие крутые фишки, но думаю этого достаточно в качестве тестового задания.
RestAPI может быть доделан, чтобы была возможность добавить мобильное приложение или что-то подобное.

## О проекте
Barter Platform - это минимально жизнеспособный продукт (MVP) платформы для обмена товарами. Пользователи могут создавать объявления о своих товарах и предлагать обмены с другими пользователями.

### Текущий функционал
- Регистрация и аутентификация пользователей
- Создание, редактирование и удаление объявлений
- Просмотр списка объявлений с фильтрацией по категориям и условиям
- Создание предложений обмена между пользователями
- Просмотр деталей предложений и управление их статусом

### Технологии
- Backend: Django 5.0
- База данных: PostgreSQL
- Frontend: HTML, CSS, Bootstrap
- Шаблонизация: Jinja2
- Контейнеризация: Docker, Docker Compose

## Возможные улучшения
### Функциональные улучшения
- [ ] Реализация REST API для мобильного приложения
- [ ] Система уведомлений о новых предложениях
- [ ] Чат между пользователями
- [ ] Система рейтинга пользователей
- [ ] Модерация объявлений
- [ ] Расширенная система категорий
- [ ] Поиск по геолокации
- [ ] Система отзывов после обмена

### Технические улучшения
- [ ] Улучшенная валидация данных
- [ ] Тестирование (unit tests, integration tests)
- [ ] CI/CD пайплайн
- [ ] Мониторинг и логирование
- [ ] Кэширование
- [ ] Оптимизация запросов к БД
- [ ] Rate limiting для API



## Установка и запуск

### Предварительные требования
- Docker
- Docker Compose
- Python 3.12 (для локальной разработки)

### Запуск через Docker
1. Клонируйте репозиторий:
```bash
git clone https://github.com/A7med373/barter_platform.git
cd barter_platform
```

2. Создайте файл `.env` в корне проекта от файла `.env.example`:
```bash
# Django
DJANGO_SECRET_KEY=vash-krutoy-kluch
DEBUG=1

# Postgres
DB_HOST=db
DB_PORT=5432

DATABASE_URL=postgres://postgres:Hgyhgdhgyhgd11!@db:5432/barter_platform

POSTGRES_USER=django_user
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_DB=django

```

3. Запустите проект:
```bash
docker-compose up --build
```


4. Создайте суперпользователя:
```bash
docker-compose exec backend python manage.py createsuperuser
```

Проект будет доступен по адресу: http://localhost

### Локальная разработка
1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройте базу данных PostgreSQL и обновите настройки в `barter_platform/settings.py`

4. Примените миграции:
```bash
python manage.py migrate
```

5. Запустите сервер разработки:
```bash
python manage.py runserver
```

## Структура проекта
```
barter_platform/
├── apps/
│   ├── accounts/      # Приложение для управления пользователями
│   └── ads/           # Приложение для объявлений и предложений
├── templates/         # Шаблоны Jinja2
├── barter_platform/   # Настройки проекта
├── docker-compose.yml # Конфигурация Docker
├── Dockerfile        # Конфигурация Docker для backend
└── nginx.conf        # Конфигурация Nginx
```


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
```
