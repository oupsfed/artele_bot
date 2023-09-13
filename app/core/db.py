import os

from dotenv import load_dotenv
from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base, declared_attr

load_dotenv()

Base = declarative_base()
DB_URL = os.getenv('DB_URL')


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)
