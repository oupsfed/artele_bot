from sqlalchemy import Column, String, Integer, Text

from app.core.db import Base


class Item(Base):
    name = Column(String(56))
    description = Column(Text())
    weight = Column(Integer())
    price = Column(Integer())
    image = Column(Text())

    def __repr__(self):
        return self.name
