from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///to_do_list.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def create_db():
    # Імпортуємо всі моделі перед create_all
    from models.user import User
    from models.task import Task
    Base.metadata.create_all(bind=engine)

def drop_db():
    from models.user import User
    from models.task import Task
    Base.metadata.drop_all(bind=engine)
