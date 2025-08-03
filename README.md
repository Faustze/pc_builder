# PC Builder Project

## Обзор

Это веб-приложение на Flask для сборки и управления компонентами ПК: материнскими платами, процессорами, видеокартами, оперативной памятью и др. Проверяется совместимость компонентов.

---

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

В консоли PostgreSQL:

```sql
CREATE USER yourusername WITH PASSWORD 'yourpassword';
CREATE DATABASE yourdbname OWNER yourusername;
```

2. **Разреши подключение по паролю**:

Открой файл `/etc/postgresql/15/main/pg_hba.conf` (или соответствующий для твоей системы):

```conf
# Найди строчку:
host    all             all             127.0.0.1/32            peer

# Замени на:
host    all             all             127.0.0.1/32            md5
```

3. Перезапусти PostgreSQL:

```bash
sudo service postgresql restart
```

---

## Структура проекта

```text
pc_builder/
├── app/                         # Основное приложение
├── alembic/                     # Миграции БД
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py                       # Точка входа
└── venv/                        # Виртуальное окружение (если не Docker)
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
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows
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
DB_USER=yourusername
DB_PASS=yourpassword
DB_NAME=yourdbname
DB_HOST=localhost   # или db, если через Docker
DB_PORT=5432
FLASK_ENV=development
SECRET_KEY=your_secret_key
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