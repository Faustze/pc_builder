import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker


database_url = os.getenv("DATABASE_URL")

engine = create_engine(
    url=database_url,
    echo=False,
    pool_size=5,
    max_overflow=10,
)

session_factory = sessionmaker(engine, autoflush=False, autocommit=False, future=True)


class BaseModel(DeclarativeBase):
    repr_cols_num = 3
    repr_cols = ()

    def __repr__(self):
        """
        Return a string representation of the object containing selected model attributes.
        Generates a string in the format `<Class: attribute=value,...>`, where:
            - Class is the model class name (e.g., `Motherboard`, `CPU`).
            - Attributes are chosen from:
        1. The explicit list `repr_cols` (e.g., `repr_cols = ['id', 'socket_type_id']`),
        2. The first `repr_cols_num` attributes if `repr_cols` is not defined.

        Example output:
            `<Motherboard id=1, socket_type_id=2, ...>`
        """
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {','.join(cols)}>"


Base = BaseModel


def drop_all_tables_cascade():
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        conn.commit()
