from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("sqlite:///to_do_list.db")
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    ...


def create_db():
    Base.metadata.create_all(engine)


def drop_db():

    Base.metadata.drop_all(engine)