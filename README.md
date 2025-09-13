# PCBuilder

## Обзор
Это веб-приложение для сборки и управления компонентами ПК: материнские платы, процессоры, видеокарты, оперативная память и т.д.

Возможности: 
   1) Проверка совместимости компонентов/классификаторов по характеристикам;
   2) Добавление своих компонентов/классификаторов/сборок;

## Стек-технологий
Backend - Python, Flask, SQLAlchemy, Alembic, PostgreSQL
Frontend - HTML, CSS, Jinja2, Bootstrap 5

## Визуальное представление приложения


## Структура проекта

```text
├── app
│   ├── __init__.py       # Создание приложения
│   ├── config.py         # Настройки приложения
│   ├── database_data.py  # Создание примеров сборок/комплектующих/классификаторов компьютеров
│   ├── database.py       # Настройка SQLAlchemy
│   ├── forms.py          # Валидация моделей с помощью Flask-WTForms
│   ├── models.py         # Модели SQLAlchemy
│   ├── routes.py         # Flask CRUD API
│   ├── static            # CSS
│   └── templates         # HTML
├── docker-compose.yml    # Конфигурация приложения для Docker
├── Dockerfile            # Инструкции по созданию Docker образа
├── README.md             # Описание проекта
├── requirements.txt      # Используемые зависимости
└── run.py                # Точка входа в проект
```

### 1. Установите Docker

* Docker: [https://www.docker.com/](https://www.docker.com/)

### 2. Выполните команду в терминале, для создания Docker образа

Для Linux/MacOS/Windows:
```
docker compose up --build
```

### 3. Перейдите по ссылке:
   [http://127.0.0.1:8000](http://127.0.0.1:8000)