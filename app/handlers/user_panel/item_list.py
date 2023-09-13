from aiogram import Router, types, F
from aiogram.filters import Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.actions import item_action
from app.core.factories import ItemCallbackFactory
from app.crud.item import item_crud

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
        item_data = await item_crud.get(callback_data.id,
                                        session=session)
        print(item_data)
        message_text = (f"<b>{item_data.name}</b> \n"
                        f"{item_data.description} \n"
                        f"Вес: {item_data.weight} г. \n"
                        f"Цена: {item_data.price} ₽")
        await callback.message.answer(
            text=message_text,
            # reply_markup=builder.as_markup()
        )
        await callback.message.delete()
