from sqlalchemy import Column, Integer, ForeignKey, BigInteger
from sqlalchemy.orm import Relationship

from app.core.db import Base
from app.models.item import Item


class Cart(Base):
    user_id = Column(BigInteger, ForeignKey('user.telegram_chat_id'))
    item_id = Column(Integer, ForeignKey('item.id'))
    item = Relationship(Item, backref='cart',)
    amount = Column(Integer, default=1)

    def __repr__(self):
        return self.user_id
