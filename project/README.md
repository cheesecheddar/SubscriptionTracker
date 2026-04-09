# SubscriptionTracker Bot

Telegram-бот для отслеживания и управления подписками пользователя. Бот позволяет добавлять подписки, просматривать активные, получать напоминания о предстоящих списаниях и вести статистику расходов.

## Возможности

- Добавление подписок с указанием названия, стоимости и даты списания
- Просмотр списка активных подписок
- Удаление подписок
- Расчёт суммарных расходов за месяц
- Напоминания о предстоящих списаниях

## Технологии

- Python 3.10+
- python-telegram-bot — взаимодействие с Telegram Bot API
- SQLite (через sqlite3) — хранение данных
- APScheduler — планировщик напоминаний

## Зависимости

Все зависимости перечислены в файле `requirements.txt`. Основные:

| Пакет                | Назначение                  |
|----------------------|-----------------------------|
| python-telegram-bot  | Telegram Bot API            |
| APScheduler          | Планировщик задач           |
| python-dotenv        | Загрузка переменных окружения |

## Установка и запуск

```bash
# 1. Клонировать репозиторий
git clone git@github.com:cheesecheddar/SubscriptionTracker.git
cd SubscriptionTracker

# 2. Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Создать файл .env по образцу
cp .env.example .env
# Укажите BOT_TOKEN в файле .env

# 5. Запустить бота
python -m subscription_tracker
```

## Сборка пакета

```bash
pip install build
python -m build
```

## Сборка документации

```bash
cd docs
make html
```

Документация будет доступна в `docs/_build/html/index.html`.

## Структура проекта

```
SubscriptionTracker/
├── subscription_tracker/   # Исходный код пакета
│   ├── __init__.py
│   ├── __main__.py         # Точка входа
│   ├── bot.py              # Обработчики команд бота
│   ├── database.py         # Работа с БД (SQLite)
│   └── models.py           # Модели данных
├── tests/                  # Тесты
│   └── test_database.py
├── docs/                   # Sphinx-документация
│   ├── conf.py
│   ├── index.rst
│   └── Makefile
├── requirements.txt
├── setup.py
├── pyproject.toml
├── .env.example
├── .gitignore
└── README.md
```

## Автор

Студент группы ИКБО-42-24, ИИТ, РТУ МИРЭА
