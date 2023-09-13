from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.item import Item


class CRUDItem(CRUDBase):
    async def get_multi_limit(
            self,
            session: AsyncSession,
    ):
        result = await session.execute(select(Item))

        return result.scalars().all()


item_crud = CRUDItem(Item)
