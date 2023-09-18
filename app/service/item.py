from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.actions import item_action
from app.core.factories import ItemCallbackFactory
from app.crud.cart import cart_crud
from app.crud.item import item_crud

ITEM_COL = {
    'name': 'название',
    'description': 'описание',
    'weight': 'масса',
    'price': 'цена',
    'image': 'фото'
}


# async def item_list_builder(item_data: dict,
#                             offset: int = 0,
#                             admin: bool = False) -> InlineKeyboardBuilder:
#     """
#     Функция формирования кнопок для меню товаров.
#
#             Parameters:
#                     json_response (dict) : словарь ответа API товаров
#                     pagination (bool) : включена ли пагинация в проекте
#                     admin (bool): подключать ли функции администратора
#
#             Returns:
#                     builder (InlineKeyboardBuilder): объект кнопок
#     """
#     builder = InlineKeyboardBuilder()
#     rows = []
#     for item in item_data:
#         btn_text = f"{item['name']} - {item['price']} ₽"
#         builder.button(
#             text=btn_text,
#             callback_data=FoodCallbackFactory(
#                 action=food_action.get,
#                 page=page,
#                 id=item['id'])
#         )
#         rows.append(1)
#     page_buttons, builder = await paginate_builder(
#         json_response,
#         builder,
#         FoodCallbackFactory,
#         food_action.get_all
#     )
#     if page_buttons > 0:
#         rows.append(page_buttons)
#     if admin:
#         builder.button(
#             text="Добавить товар",
#             callback_data=FoodCallbackFactory(
#                 action=food_action.create_preview,
#                 page=page)
#         )
#         rows.append(1)
#     builder.adjust(*rows)
#     return builder


# async def food_info(food: dict) -> dict:
#     """
#     Функция формирования текста сообщения определенного товара.
#
#             Parameters:
#                     food (dict) : словарь товара
#
#             Returns:
#                     data (dict): словарь содержащий текст и изображение товара
#     """
#     text = (f"<b>{food['name']}</b> \n"
#             f"{food['description']} \n"
#             f"Вес: {food['weight']} г. \n"
#             f"Цена: {food['price']} ₽")
#     food_image = URLInputFile('https://agentura-soft.ru/images/noImage.png')
#     if food['image']:
#         food_image = URLInputFile(food['image'])
#     return {
#         'text': text,
#         'image': food_image
#     }


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
    # food_price = food['price']
    # if 'results' in cart:
    #     cart = cart['results']
    #     if len(cart) > 0:
    #         cart = cart[0]
    # if 'amount' in cart:
    #     amount = cart['amount']
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
    # builder = await back_builder(
    #     builder,
    #     item_action.get_all,
    # )
    rows.append(1)
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
    builder.adjust(*rows)
    return builder


async def edit_item_preview_builder(item_id: int,
                                    page: int = 1):
    """
    Функция формирования кнопок для редактирования товара.

            Parameters:
                    food_id (int) : id объекта Food
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
