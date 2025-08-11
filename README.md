# PC Builder Project

## Обзор

Это веб-приложение на Flask для сборки и управления компонентами ПК: материнскими платами, процессорами, видеокартами, оперативной памятью и др. Проверяется совместимость компонентов.

---

## Структура проекта

```text
pc_builder/
├── app/                         # Основное приложение
├── alembic/                     # Миграции БД
├── docker-compose.yml           # Конфигурация приложения
├── Dockerfile                   # Инструкции для сборки docker образа
├── requirements.txt             # Версии зависимостей
├── run.py                       # Точка входа
└── venv/                        # Виртуальное окружение (если не Docker)
```

## Что нужно сделать перед запуском (обязательно прочти!)

### 1. Установи Docker и Python

* Docker: [https://www.docker.com/](https://www.docker.com/)
* Python 3.12+: [https://www.python.org/](https://www.python.org/)

---

### 2. Настрой PostgreSQL (если запускаешь без Docker)

Если запускаешь **локально**, не в контейнере, тебе нужно вручную настроить PostgreSQL:

1. **Создай нового пользователя и базу данных**:

```bash
sudo -u postgres psql
```
(Будем пользоваться суперпользователем "из коробки" для упрощения)

В консоли PostgreSQL:

```sql
CREATE DATABASE pc_builder_db;
```

2. **Разреши подключение по паролю**:

Открой файл `/etc/postgresql/15/main/pg_hba.conf` (или соответствующий для твоей системы):

```conf
# Найди строчку:
host    all             all             127.0.0.1/32            peer

# Замени на:
host    all             all             127.0.0.1/32            trust
```

```bash
psql -U postgres
```
```psql
ALTER USER postgres WITH PASSWORD 'password';
\q
```

3. **Поменяй подключение на подключение с паролем**:
Открой файл `/etc/postgresql/15/main/pg_hba.conf` (или соответствующий для твоей системы):

```conf
# Замени на:
host    all             all             127.0.0.1/32            md5
```

3. **Перезапусти PostgreSQL**:

```bash
sudo systemctl restart postgresql
```

---

## Запуск с Docker

1. Убедись, что в `.env` прописан хост базы как `db`:

```ini
DB_HOST=db
```

2. Собери и запусти контейнеры:

```bash
sudo docker-compose up --build
```

3. Открой приложение в браузере:
   [http://localhost:8000](http://localhost:8000)

---

## Запуск без Docker (локально)

1. В `.env` укажи:

```ini
DB_HOST=localhost
```

2. Создай и активируй виртуальное окружение:

```bash
sudo apt update
python -m venv venv
source venv/bin/activate       # Linux/macOS
```

3. Установи зависимости:

```bash
pip install -r requirements.txt
```

4. Примени миграции:

```bash
alembic upgrade head
```

5. Запусти приложение:

```bash
python run.py
```

6. Открой приложение в браузере:
   [http://localhost:8000](http://localhost:8000)

---

## Переменные окружения `.env`

```ini
DB_HOST=localhost   # или db, если через Docker
DB_PORT=5432
DB_USER=postgres
DB_PASS=password
DB_NAME=pc_builder_db

DEBUG=true
SECRET_KEY=dev_key

FLASK_APP=app
FLASK_ENV=development

USE_ALEMBIC=true
```

---

## Миграции Alembic

* Создать новую миграцию:

```bash
alembic revision -m "описание"
```

* Применить все миграции:

```bash
alembic upgrade head
```

