import os
import sys
from logging.config import fileConfig

<<<<<<< HEAD
from dotenv import load_dotenv
=======
>>>>>>> 7037c3bb92fa73555548885498969c103a4342c1
from sqlalchemy import engine_from_config, pool

from alembic import context

<<<<<<< HEAD
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import Base  # noqa: E402
from app.models import *  # noqa: F401, F403, E402
=======
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import models  # noqa: F401, E402
from app.database import Base  # noqa: E402
>>>>>>> 7037c3bb92fa73555548885498969c103a4342c1

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

<<<<<<< HEAD
db_url = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

config.set_main_option("sqlalchemy.url", db_url)

=======
>>>>>>> 7037c3bb92fa73555548885498969c103a4342c1
target_metadata = Base.metadata


def run_migrations_offline():
<<<<<<< HEAD
=======
    """Миграции в offline режиме — без подключения к базе."""
>>>>>>> 7037c3bb92fa73555548885498969c103a4342c1
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
<<<<<<< HEAD
=======
    """Миграции в online режиме — с подключением к базе."""
>>>>>>> 7037c3bb92fa73555548885498969c103a4342c1
    section = config.get_section(config.config_ini_section)

    if section is None:
        raise ValueError("Конфигурационный раздел не найден.")

    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
<<<<<<< HEAD
=======

print("Tables discovered by Alembic:")
print(target_metadata.tables.keys())
>>>>>>> 7037c3bb92fa73555548885498969c103a4342c1
