from enum import Enum

from sqlalchemy import Column, BigInteger, String, Integer
from sqlalchemy_utils import ChoiceType

from app.core.db import Base


class Role(Enum):
    guest = 'Guest'
    user = 'User'
    admin = 'Admin'


class User(Base):
    telegram_chat_id = Column(BigInteger, unique=True)
    first_name = Column(String(200), default='Неизвестный пользователь')
    last_name = Column(String(200), nullable=True)
    username = Column(String(200), nullable=True)
    role = Column(ChoiceType(Role), default=Role.guest)

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'
