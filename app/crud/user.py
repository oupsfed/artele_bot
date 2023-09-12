from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.user import User


class CRUDUser(CRUDBase):

    async def check_user_exists(
            self,
            user_id: int,
            session: AsyncSession,
    ):
        result = await session.execute(
            select(
                select(User).where(User.telegram_chat_id == user_id).exists()
            ))
        return result.scalar()

    async def get_user_role(
            self,
            user_id: int,
            session: AsyncSession,
    ):
        result = await session.execute(
            select(User.role).where(User.telegram_chat_id == user_id)
            )
        return result.scalar()


user_crud = CRUDUser(User)
