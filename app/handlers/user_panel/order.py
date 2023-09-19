from aiogram import Bot, Router, types
from aiogram.filters import Text
from magic_filter import F
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.actions import order_action
from app.core.factories import OrderCallbackFactory
from app.service.order import order_create

router = Router()


# @router.message(Text('Заказ'))
# async def order(message: types.Message):
#     order_id, text = await order_info(message.from_user.id)
#     builder = await order_builder(order_id)
#     await message.answer(
#         text,
#         reply_markup=builder.as_markup()
#     )


@router.callback_query(OrderCallbackFactory.filter(F.action == order_action.create))
async def callbacks_show_cart(
        callback: types.CallbackQuery,
        callback_data: OrderCallbackFactory,
        session: AsyncSession
):
    message_text = await order_create(
        user_id=callback.from_user.id,
        session=session
    )
    await callback.message.delete()
    await callback.message.answer(
        message_text
    )


# @router.callback_query(OrderCallbackFactory.filter(F.action == order_action.remove))
# async def callbacks_order_cancel(
#         callback: types.CallbackQuery,
#         callback_data: OrderCallbackFactory
# ):
#     answer, text = await order_update(callback_data.order_id,
#                                       status='cancelled')
#     await callback.message.delete()
#     await callback.message.answer(
#         text
#     )