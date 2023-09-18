from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import user_crud
from app.models.user import Role


async def is_admin(user_id,
                   session: AsyncSession) -> bool:
    """
    Валидатор проверки прав администратора

            Parameters:
                    user_id (int) : telegram-chat-id пользователя
                    session (AsyncSession) : объект сессии

            Returns:
                    answer (bool): Возвращает True, False
    """
    return await user_crud.get_user_role(user_id, session) == Role.admin


async def is_guest(user_id,
                   session: AsyncSession) -> bool:
    """
    Валидатор проверки прав гостя

            Parameters:
                    user_id (int) : telegram-chat-id пользователя
                    session (AsyncSession) : объект сессии

            Returns:
                    answer (bool): Возвращает True, False
    """
    return await user_crud.get_user_role(user_id, session) == Role.guest


class IsAdminMessageMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        if await is_admin(event.chat.id,
                          data['session']):
            return await handler(event, data)
        await event.answer(
            "Доступ только для администратора",
            show_alert=True
        )
        return False


class IsAdminCallbackMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        if await is_admin(event.chat.id,
                          data['session']):
            return await handler(event, data)
        await event.answer(
            "Доступ только для администратора",
            show_alert=True
        )
        return False


class IsGuestMessageMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if await is_guest(event.chat.id,
                          data['session']):
            return await handler(event, data)
        await event.answer(
            "Доступ только для гостей",
            show_alert=True
        )
        return False


class IsGuestCallbackMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        if await is_guest(event.chat.id,
                          data['session']):
            return await handler(event, data)
        await event.answer(
            "Доступ только для гостей",
            show_alert=True
        )
        return False
