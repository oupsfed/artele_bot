from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.cart import Cart


class CRUDCART(CRUDBase):
    async def get_multi_limit(
            self,
            session: AsyncSession,
    ):
        result = await session.execute(select(Cart))

        return result.scalars().all()

    async def get_direct_cart(
            self,
            user_id: int,
            item_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(Cart).filter(and_(Cart.user_id == user_id,
                                     Cart.item_id == item_id))
        )
        return db_obj.scalars().first()

    async def add_amount(
            self,
            db_obj,
            session: AsyncSession,
    ):
        db_obj.amount += 1
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove_amount(
            self,
            db_obj,
            session: AsyncSession,
    ):
        db_obj.amount -= 1
        if db_obj.amount == 0:
            await session.delete(db_obj)
            await session.commit()
            return db_obj
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


cart_crud = CRUDCART(Cart)
