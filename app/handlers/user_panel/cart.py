from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from magic_filter import F
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.actions import cart_action
from app.core.factories import CartCallbackFactory
from app.service.cart import cart_list_builder, add_to_cart, remove_from_cart
from app.service.item import item_info

router = Router()

MAIN_MESSAGE = 'Корзина:'


@router.message(Text('Корзина'))
async def menu(message: types.Message,
               session: AsyncSession):
    user_id = message.from_user.id
    builder = await cart_list_builder(user_id,
                                      session)
    await message.answer(
        MAIN_MESSAGE,
        reply_markup=builder.as_markup()
    )


@router.callback_query(CartCallbackFactory.filter(F.action == cart_action.get_all))
async def callbacks_show_cart(
        callback: types.CallbackQuery,
        callback_data: CartCallbackFactory,
        session: AsyncSession
):
    user_id = callback.from_user.id
    builder = await cart_list_builder(user_id,
                                      session,
                                      offset=callback_data.offset)
    if callback.message.photo:
        await callback.message.delete()
        await callback.message.answer(
            MAIN_MESSAGE,
            reply_markup=builder.as_markup()
        )
    else:
        await callback.message.edit_reply_markup(
            reply_markup=builder.as_markup()
        )


@router.callback_query(CartCallbackFactory.filter(F.action == cart_action.get))
async def callbacks_show_item(
        callback: types.CallbackQuery,
        callback_data: CartCallbackFactory,
        session: AsyncSession
):
    message_text, image_data = await item_info(callback_data.id,
                                               session)
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Назад',
        callback_data=CartCallbackFactory(
            action=cart_action.get_all
        ))
    builder.adjust(1)
    await callback.message.answer_photo(
        image_data,
        caption=message_text,
        reply_markup=builder.as_markup()
    )
    await callback.message.delete()


@router.callback_query(CartCallbackFactory.filter(F.action == cart_action.create))
async def callbacks_add_to_cart(
        callback: types.CallbackQuery,
        callback_data: CartCallbackFactory,
        session: AsyncSession
):
    user_id = callback.from_user.id
    item_id = callback_data.item_id
    await add_to_cart(
        user_id=user_id,
        item_id=item_id,
        session=session
    )
    builder = await cart_list_builder(user_id,
                                      session,
                                      offset=callback_data.offset)
    await callback.message.edit_reply_markup(
        reply_markup=builder.as_markup()
    )


@router.callback_query(CartCallbackFactory.filter(F.action == cart_action.remove))
async def callbacks_delete_from_cart(
        callback: types.CallbackQuery,
        callback_data: CartCallbackFactory,
        session: AsyncSession
):
    user_id = callback.from_user.id
    item_id = callback_data.item_id
    await remove_from_cart(
        user_id=user_id,
        item_id=item_id,
        session=session
    )
    builder = await cart_list_builder(user_id,
                                      session,
                                      offset=callback_data.offset)
    await callback.message.edit_reply_markup(
        reply_markup=builder.as_markup()
    )
