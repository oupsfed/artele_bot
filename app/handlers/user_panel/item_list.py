from aiogram import Router, types, F
from aiogram.filters import Text
from aiogram.types import FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.actions import item_action
from app.core.factories import ItemCallbackFactory
from app.crud.item import item_crud
from app.middlewares.role import is_admin
from app.service.cart import add_to_cart, remove_from_cart
from app.service.item import item_get_builder, item_list_builder

router = Router()

MAIN_MESSAGE = 'Меню:'


@router.message(Text('Меню'))
async def item_list(message: types.Message,
                    session: AsyncSession):
    admin = await is_admin(message.from_user.id,
                           session)
    builder = await item_list_builder(session,
                                      offset=0,
                                      admin=admin)
    await message.answer(
        MAIN_MESSAGE,
        reply_markup=builder.as_markup()
    )


@router.callback_query(ItemCallbackFactory.filter(F.action == item_action.get_all))
async def callback_item_list(
        callback: types.CallbackQuery,
        callback_data: ItemCallbackFactory,
        session: AsyncSession
):
    admin = await is_admin(callback.from_user.id,
                           session)
    builder = await item_list_builder(session,
                                      offset=callback_data.offset,
                                      admin=admin)
    await callback.message.edit_reply_markup(
        reply_markup=builder.as_markup()
    )


@router.callback_query(ItemCallbackFactory.filter(F.action == item_action.get))
async def item_get(
        callback: types.CallbackQuery,
        callback_data: ItemCallbackFactory,
        session: AsyncSession
):
    admin = await is_admin(callback.from_user.id,
                           session)
    item_data = await item_crud.get(callback_data.id,
                                    session=session)
    image_data = FSInputFile('static/no_image.png')
    if item_data.image:
        image_data = FSInputFile(f'media/{item_data.image}')
    message_text = (f"<b>{item_data.name}</b> \n"
                    f"{item_data.description} \n"
                    f"Вес: {item_data.weight} г. \n"
                    f"Цена: {item_data.price} ₽")
    builder = await item_get_builder(item_data.id,
                                     callback.from_user.id,
                                     session,
                                     admin=admin)
    await callback.message.answer_photo(
        photo=image_data,
        caption=message_text,
        reply_markup=builder.as_markup()
    )
    await callback.message.delete()


@router.callback_query(ItemCallbackFactory.filter(F.action == item_action.add_to_cart))
async def item_add_to_cart(
        callback: types.CallbackQuery,
        callback_data: ItemCallbackFactory,
        session: AsyncSession
):
    user_id = callback.from_user.id
    item_id = callback_data.id
    admin = await is_admin(user_id=user_id,
                           session=session)
    await add_to_cart(
        user_id=user_id,
        item_id=item_id,
        session=session
    )
    builder = await item_get_builder(item_id=item_id,
                                     user_id=user_id,
                                     session=session,
                                     admin=admin)
    await callback.message.edit_reply_markup(
        reply_markup=builder.as_markup()
    )


@router.callback_query(ItemCallbackFactory.filter(F.action == item_action.remove_from_cart))
async def item_remove_from_cart(
        callback: types.CallbackQuery,
        callback_data: ItemCallbackFactory,
        session: AsyncSession
):
    user_id = callback.from_user.id
    item_id = callback_data.id
    admin = await is_admin(user_id=user_id,
                           session=session)
    await remove_from_cart(
        user_id=user_id,
        item_id=item_id,
        session=session
    )
    builder = await item_get_builder(item_id=item_id,
                                     user_id=user_id,
                                     session=session,
                                     admin=admin)
    await callback.message.edit_reply_markup(
        reply_markup=builder.as_markup()
    )
