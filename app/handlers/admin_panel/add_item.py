from aiogram import Bot, F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.actions import item_action
from app.core.factories import ItemCallbackFactory
from app.crud.item import item_crud
from app.middlewares.role import IsAdminMessageMiddleware

router = Router()
router.message.middleware(IsAdminMessageMiddleware())


class AddFood(StatesGroup):
    name = State()
    description = State()
    weight = State()
    price = State()
    image = State()


@router.callback_query(ItemCallbackFactory.filter(F.action == item_action.create_preview))
async def callbacks_add_food_name(
        callback: types.CallbackQuery,
        state: FSMContext,
        session: AsyncSession
):
    await callback.message.answer(
        text='Введите название товара',
    )
    await state.set_state(AddFood.name)


@router.message(AddFood.name)
async def callbacks_add_food_description(
        message: Message,
        state: FSMContext,
        session: AsyncSession
):
    await state.update_data(name=message.text)
    await message.answer(
        text='Введите описание товара',
    )
    await state.set_state(AddFood.description)


@router.message(AddFood.description)
async def callbacks_add_food_weight(
        message: Message,
        state: FSMContext,
        session: AsyncSession
):
    await state.update_data(description=message.text)
    await message.answer(
        text='Введите вес товара в граммах',
    )
    await state.set_state(AddFood.weight)


@router.message(AddFood.weight)
async def callbacks_add_food_price(
        message: Message,
        state: FSMContext,
        session: AsyncSession
):
    await state.update_data(weight=message.text)
    await message.answer(
        text='Введите цену товара',
    )
    await state.set_state(AddFood.price)


@router.message(AddFood.price)
async def callbacks_add_food_image(
        message: Message,
        state: FSMContext,
        session: AsyncSession
):
    await state.update_data(price=message.text)
    await message.answer(
        text='Добавьте фото товара',
    )
    await state.set_state(AddFood.image)


@router.message(AddFood.image)
async def callbacks_add_food_confirm(
        message: Message,
        state: FSMContext,
        bot: Bot,
        session: AsyncSession
):
    img_name = f'{message.photo[-1].file_id}.png'
    await bot.download(file=message.photo[-1],
                       destination=f'media/{img_name}')
    await state.update_data(image=img_name)
    data = await state.get_data()
    item_data = await item_crud.create(data,
                                       session)
    image_data = FSInputFile('static/no_image.png')
    if item_data.image:
        image_data = FSInputFile(f'media/{item_data.image}')
    message_text = (f"<b>{item_data.name}</b> \n"
                    f"{item_data.description} \n"
                    f"Вес: {item_data.weight} г. \n"
                    f"Цена: {item_data.price} ₽")
    await message.answer_photo(
        photo=image_data,
        caption=message_text,
        # reply_markup=builder.as_markup()
    )
    await state.clear()
