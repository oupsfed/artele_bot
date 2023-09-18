from sqlalchemy import Column, Integer, ForeignKey, BigInteger

from app.core.db import Base


class Cart(Base):
    user_id = Column(BigInteger, ForeignKey('user.telegram_chat_id'))
    item_id = Column(Integer, ForeignKey('item.id'))
    amount = Column(Integer, default=1)

    def __repr__(self):
        return self.user_id
