import base64

from aiogram import Router, types, F
from aiogram.filters import Text
from aiogram.types import InputFile, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.actions import item_action
from app.core.factories import ItemCallbackFactory
from app.crud.item import item_crud
from app.middlewares.role import is_admin
from app.service.cart import add_to_cart, remove_from_cart
from app.service.item import item_get_builder

router = Router()

MAIN_MESSAGE = 'Меню:'


@router.message(Text('Меню'))
async def item_list(message: types.Message,
                    session: AsyncSession):
    items_data = await item_crud.get_multi_limit(session=session)
    builder = InlineKeyboardBuilder()
    rows = []
    for item in items_data:
        btn_text = f"{item.name} - {item.price} ₽"
        builder.button(
            text=btn_text,
            callback_data=ItemCallbackFactory(
                action=item_action.get,
                page=1,
                id=item.id)
        )
        rows.append(1)
    if await is_admin(message.from_user.id,
                      session):
        builder.button(
            text='Добавить товар',
            callback_data=ItemCallbackFactory(
                action=item_action.create_preview,
            )
        )
        rows.append(1)
    builder.adjust(*rows)
    await message.answer(
        MAIN_MESSAGE,
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
