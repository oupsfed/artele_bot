from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.item import Item


class CRUDItem(CRUDBase):
    async def get_multi_limit(
            self,
            limit: int,
            offset: int,
            session: AsyncSession,
    ):
        result = await session.execute(select(Item).limit(limit).offset(offset))

        return result.scalars().all()


item_crud = CRUDItem(Item)
