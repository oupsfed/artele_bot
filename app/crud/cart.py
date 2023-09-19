from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.cart import Cart
from app.models.item import Item
from app.utils import PAGE_LIMIT


class CRUDCART(CRUDBase):

    async def get_user_cart(
            self,
            user_id: int,
            session: AsyncSession,
            offset: int = 0,
            limit: int = PAGE_LIMIT
    ):
        db_obj = await session.execute(
            select(Cart)
            .filter(Cart.user_id == user_id)
            .options(selectinload(Cart.item))
            .limit(limit)
            .offset(offset)
        )
        return db_obj.scalars().all()

    async def count_user_cart(
            self,
            user_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(Cart.id).filter(Cart.user_id == user_id)
        )
        return len(db_obj.scalars().all())

    async def sum_user_cart(
            self,
            user_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(func.sum(
                Cart.amount
                * select(
                    Item.price
                ).where(Item.id == Cart.item_id).scalar_subquery())
                   .filter(Cart.user_id == user_id)
                   )
        )

        return db_obj.scalars().first()

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
