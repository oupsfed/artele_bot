from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.item import Item


class CRUDItem(CRUDBase):
    pass


item_crud = CRUDItem(Item)
