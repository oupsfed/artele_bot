from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.actions import item_action
from app.core.builders import paginate_builder, back_builder
from app.core.factories import ItemCallbackFactory
from app.crud.cart import cart_crud
from app.crud.item import item_crud
from app.utils import PAGE_LIMIT

ITEM_COL = {
    'name': 'название',
    'description': 'описание',
    'weight': 'масса',
    'price': 'цена',
    'image': 'фото'
}


async def item_list_builder(session: AsyncSession,
                            offset: int = 0,
                            admin: bool = False) -> InlineKeyboardBuilder:
    """
    Функция формирования кнопок для меню товаров.

            Parameters:
                    session (AsyncSession) : сессия работы с БД
                    offset (int) = 0 : количетсво пропущенных записей
                    admin (bool): подключать ли функции администратора

            Returns:
                    builder (InlineKeyboardBuilder): объект кнопок
    """
    items_data = await item_crud.get_multi_limit(session=session,
                                                 limit=PAGE_LIMIT,
                                                 offset=offset)
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
    count = await item_crud.count(session=session)
    page_buttons, builder = await paginate_builder(
        offset=offset,
        count=count,
        builder=builder,
        action=item_action.get_all
    )
    if page_buttons > 0:
        rows.append(page_buttons)
    if admin:
        builder.button(
            text='Добавить товар',
            callback_data=ItemCallbackFactory(
                action=item_action.create_preview,
            )
        )
        rows.append(1)

    builder.adjust(*rows)
    return builder


async def item_info(item_id: int,
                    session: AsyncSession) -> dict:
    """
    Функция формирования текста сообщения определенного товара.

            Parameters:
                    item_id (dict) : словарь товара
                    session (AsyncSession) : сессия работы с БД

            Returns:
                    data (dict): словарь содержащий текст и изображение товара
    """
    item_data = await item_crud.get(item_id,
                                    session=session)
    image_data = FSInputFile('static/no_image.png')
    if item_data.image:
        image_data = FSInputFile(f'media/{item_data.image}')
    message_text = (f"<b>{item_data.name}</b> \n"
                    f"{item_data.description} \n"
                    f"Вес: {item_data.weight} г. \n"
                    f"Цена: {item_data.price} ₽")
    return message_text, image_data


async def item_get_builder(item_id: int,
                           user_id: int,
                           session: AsyncSession,
                           admin: bool = False) -> InlineKeyboardBuilder:
    """
    Функция формирования кнопок для определенного товара.

            Parameters:
                    cart (dict) : словарь ответа API корзины
                    food (bool) : словаь определенного товара
                    page (int) : страница с которой перешли в карточку товара
                    admin (bool): подключать ли функции администратора

            Returns:
                    builder (InlineKeyboardBuilder): объект кнопок
    """
    amount = 0
    item = await item_crud.get(item_id,
                               session)
    cart = await cart_crud.get_direct_cart(user_id=user_id,
                                           item_id=item_id,
                                           session=session)
    if cart:
        amount = cart.amount
    builder = InlineKeyboardBuilder()
    rows = []
    builder.button(
        text=f'{amount} шт. ({amount * item.price} ₽)',
        callback_data=ItemCallbackFactory(
            action=item_action.add_to_cart,
            id=item.id
        )
    )
    rows.append(1)
    builder.button(
        text='➖',
        callback_data=ItemCallbackFactory(
            action=item_action.remove_from_cart,
            id=item.id
        )
    )
    builder.button(
        text='➕',
        callback_data=ItemCallbackFactory(
            action=item_action.add_to_cart,
            id=item.id
        )
    )
    rows.append(2)
    if admin:
        builder.button(
            text='Редактировать товар',
            callback_data=ItemCallbackFactory(
                action=item_action.update_preview,
                id=item.id
            )
        )
        rows.append(1)
        builder.button(
            text='Удалить товар',
            callback_data=ItemCallbackFactory(
                action=item_action.remove_preview,
                id=item.id
            )
        )
        rows.append(1)
    builder = await back_builder(
        builder,
        item_action.get_all,
    )
    rows.append(1)
    builder.adjust(*rows)
    return builder


async def edit_item_preview_builder(item_id: int,
                                    page: int = 1):
    """
    Функция формирования кнопок для редактирования товара.

            Parameters:
                    item_id (int) : id объекта Item
                    page (int) : страница для возврата к меню

            Returns:
                    builder (InlineKeyboardBuilder): объект кнопок
    """
    builder = InlineKeyboardBuilder()
    for col, name in ITEM_COL.items():
        builder.button(
            text=f'Изменить {name}',
            callback_data=ItemCallbackFactory(
                action=item_action.update_column,
                column=col,
                id=item_id
            )
        )

    builder.button(
        text='Назад',
        callback_data=ItemCallbackFactory(
            action=item_action.get,
            id=item_id,
            page=page)
    )
    builder.adjust(1)
    return builder
#
#
# async def add_food_builder():
#     """
#     Функция формирования кнопок для добавления товара.
#
#             Parameters:
#
#             Returns:
#                     builder (InlineKeyboardBuilder): объект кнопок
#     """
#     builder = InlineKeyboardBuilder()
#     builder.button(
#         text='Отмена',
#         callback_data=FoodCallbackFactory(
#             action=food_action.get_all)
#     )
#     return builder
#
#
# async def encode_image(img_dir: str) -> str:
#     """
#     Функция кодирования изображения в base64.
#
#             Parameters:
#                     img_dir (str) : путь к загруженному изображению
#
#             Returns:
#                     str (str): закодированную base64 строку изображения
#     """
#     with open(img_dir, "rb") as img_file:
#         encoded_string = base64.b64encode(img_file.read())
#     os.remove(img_dir)
#     return encoded_string.decode('utf-8')
