from enum import Enum

from sqlalchemy import Column, Integer, ForeignKey, BigInteger
from sqlalchemy.orm import Relationship, relationship
from sqlalchemy_utils import ChoiceType

from app.core.db import Base
from app.models.item import Item


class Status(Enum):
    in_progress = 'In progress'
    done = 'Done'
    cancelled = 'Cancelled'


class OrderItems(Base):
    order_id = Column(Integer, ForeignKey('order.id'))
    item_id = Column(Integer, ForeignKey('item.id'))
    amount = Column(Integer, default=1)


class Order(Base):
    user_id = Column(BigInteger, ForeignKey('user.telegram_chat_id'))
    items = relationship('Item', secondary='orderitems')
    status = Column(ChoiceType(Status), default=Status.in_progress)

    def __repr__(self):
        return self.user_id
