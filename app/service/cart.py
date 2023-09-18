from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.cart import cart_crud


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
