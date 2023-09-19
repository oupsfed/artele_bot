from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.actions import item_action, cart_action, order_action
from app.core.builders import paginate_builder
from app.core.factories import ItemCallbackFactory, CartCallbackFactory, OrderCallbackFactory
from app.crud.cart import cart_crud


async def cart_list_builder(user_id: int,
                            session: AsyncSession,
                            offset: int = 0) -> InlineKeyboardBuilder:
    """
    Функция формирования кнопок для корзины.

            Parameters:
                    user_id (int) : telegram id пользователя
                    session (AsyncSession) : сессия работы с БД
                    offset (int) = 0 : количетсво пропущенных записей

            Returns:
                    builder (InlineKeyboardBuilder): объект кнопок
    """
    cart_data = await cart_crud.get_user_cart(user_id=user_id,
                                              session=session,
                                              offset=offset)
    builder = InlineKeyboardBuilder()
    rows = []
    for cart_item in cart_data:
        item = cart_item.item
        user_id = cart_item.user_id
        builder.button(
            text=f"{item.name} - {cart_item.amount} шт.",
            callback_data=CartCallbackFactory(
                action=cart_action.get,
                id=item.id
            )
        )
        rows.append(1)
        builder.button(
            text="➖",
            callback_data=CartCallbackFactory(
                action=cart_action.remove,
                item_id=item.id,
                user_id=user_id,
            )
        )
        builder.button(
            text="➕",
            callback_data=CartCallbackFactory(
                action=cart_action.create,
                item_id=item.id,
                user_id=user_id,
            )
        )
        rows.append(2)
    count = await cart_crud.count_user_cart(user_id=user_id,
                                            session=session)
    page_buttons, builder = await paginate_builder(
        offset=offset,
        count=count,
        builder=builder,
        action=cart_action.get_all
    )
    if page_buttons > 0:
        rows.append(page_buttons)
    total_price = await cart_crud.sum_user_cart(user_id=user_id,
                                                session=session)
    builder.button(
        text=f"Заказать - {total_price} ₽",
        callback_data=OrderCallbackFactory(
            action=order_action.create)
    )
    rows.append(1)
    builder.adjust(*rows)
    return builder


async def add_to_cart(user_id: int,
                      item_id: int,
                      session: AsyncSession):
    cart = await cart_crud.get_direct_cart(user_id=user_id,
                                           item_id=item_id,
                                           session=session)
    if cart:
        await cart_crud.add_amount(cart,
                                   session)
    else:
        await cart_crud.create(
            {
                'user_id': user_id,
                'item_id': item_id
            },
            session=session
        )


async def remove_from_cart(user_id: int,
                           item_id: int,
                           session: AsyncSession):
    cart = await cart_crud.get_direct_cart(user_id=user_id,
                                           item_id=item_id,
                                           session=session)
    await cart_crud.remove_amount(cart,
                                  session)
