from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.order import Order


class CRUDOrder(CRUDBase):
    pass


order_crud = CRUDOrder(Order)
