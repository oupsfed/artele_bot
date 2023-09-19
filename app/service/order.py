from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.cart import cart_crud
from app.crud.order import order_crud
from app.crud.order_items import order_items_crud
from app.middlewares.role import is_guest


async def order_create(user_id: int,
                       session: AsyncSession):
    if await is_guest(user_id=user_id,
                      session=session):
        return (
            'Недостаточно прав для оформления заказа \n'
            'Подайте заявку на доступ к заказам'
        )
    cart_data = await cart_crud.get_user_cart(
        user_id=user_id,
        session=session
    )
    order = await order_crud.create(
        {
            'user_id': user_id,
        },
        session
    )
    for cart_item in cart_data:
        await order_items_crud.create(
            {
                'item_id': cart_item.item_id,
                'order_id': order.id,
                'amount': cart_item.amount
            },
            session
        )
        await cart_crud.remove(cart_item,
                               session)

    return 'Заказ успешно создан'
