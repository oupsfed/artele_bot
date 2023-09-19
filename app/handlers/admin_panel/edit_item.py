from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.actions import item_action
from app.core.factories import ItemCallbackFactory
from app.crud.item import item_crud
from app.middlewares.role import IsAdminMessageMiddleware
from app.service.item import edit_item_preview_builder, ITEM_COL

MAIN_MESSAGE = 'Меню'

router = Router()
router.message.middleware(IsAdminMessageMiddleware())


class EditFood(StatesGroup):
    name = State()


# @router.message(Text('Редактирование меню'))
# async def admin_menu(message: types.Message):
#     builder = await menu_builder(user_id=message.from_user.id)
#
#     await message.answer(
#         MAIN_MESSAGE,
#         reply_markup=builder.as_markup()
#     )


@router.callback_query(ItemCallbackFactory.filter(F.action == item_action.update_preview))
async def edit_item_preview(
        callback: types.CallbackQuery,
        callback_data: ItemCallbackFactory
):
    builder = await edit_item_preview_builder(
        item_id=callback_data.id,
        page=callback_data.page
    )
    await callback.message.edit_reply_markup(
        reply_markup=builder.as_markup()
    )


@router.callback_query(
    ItemCallbackFactory.filter(F.action == item_action.update_column))
async def callbacks_edit_food(
        callback: types.CallbackQuery,
        callback_data: ItemCallbackFactory,
        state: FSMContext
):
    await state.update_data(id=callback_data.id,
                            col=callback_data.column)
    await callback.message.answer(
        text=f'Введите (Пришлите) {ITEM_COL[callback_data.column]}'
    )
    await state.set_state(EditFood.name)


@router.message(EditFood.name)
async def callbacks_edit_food_confirm(
        message: Message,
        state: FSMContext,
        bot: Bot,
        session: AsyncSession
):
    data = await state.get_data()
    item_id = data['id']
    if data['col'] == 'image':
        data['name'] = f'{message.photo[-1].file_id}.png'
        await bot.download(file=message.photo[-1],
                           destination=f'media/{data["name"]}')

    else:
        await state.update_data(name=message.text)
        data = await state.get_data()
    await state.clear()
    item = await item_crud.get(item_id,
                               session)
    item = await item_crud.update(item,
                                  {
                                      data['col']: data['name']
                                  },
                                  session)
    # food_data = await food_info(food_id)
    # builder = await food_builder(
    #     message.from_user.id,
    #     food_id
    # )
    # await message.answer_photo(
    #     food_data['image'],
    #     caption=(f'{FOOD_COL[data["col"]]} успешно изменено \n'
    #              f'{food_data["text"]}'),
    #     reply_markup=builder.as_markup()
    # )


@router.callback_query(ItemCallbackFactory.filter(F.action == item_action.remove_preview))
async def callbacks_delete_food(
        callback: types.CallbackQuery,
        callback_data: ItemCallbackFactory
):
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Удалить',
        callback_data=ItemCallbackFactory(
            action=item_action.remove,
            id=callback_data.id)
    )
    builder.button(
        text='Отмена',
        callback_data=ItemCallbackFactory(
            action=item_action.get,
            id=callback_data.id)
    )
    await callback.message.edit_reply_markup(
        reply_markup=builder.as_markup()
    )


@router.callback_query(ItemCallbackFactory.filter(F.action == item_action.remove))
async def callbacks_delete_food(
        callback: types.CallbackQuery,
        callback_data: ItemCallbackFactory,
        session: AsyncSession
):
    item = await item_crud.get(callback_data.id,
                               session)
    await item_crud.remove(item,
                           session)
    await callback.message.answer(
        'Товар успешно удален')
    await callback.message.delete()
