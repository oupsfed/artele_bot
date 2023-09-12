import os

from dotenv import load_dotenv
from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker


load_dotenv()

Base = declarative_base()
DB_URL = os.getenv('DB_URL')



class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)
engine = create_async_engine(DB_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)