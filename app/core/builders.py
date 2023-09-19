from app.core import factories
from app.utils import PAGE_LIMIT

CALLBACK_DATA = {
    'item': factories.ItemCallbackFactory,
    'cart': factories.CartCallbackFactory
}


async def paginate_builder(offset,
                           count,
                           builder,
                           action):
    data = action.split('-')
    page_buttons = 0
    if offset >= PAGE_LIMIT:
        builder.button(
            text="⬅️",
            callback_data=CALLBACK_DATA[data[0]](
                action=action,
                offset=offset - PAGE_LIMIT
            )
        )
        page_buttons += 1
    if offset + PAGE_LIMIT < count:
        builder.button(
            text="➡️",
            callback_data=CALLBACK_DATA[data[0]](
                action=action,
                offset=offset + PAGE_LIMIT
            )
        )
        page_buttons += 1
    return page_buttons, builder


async def back_builder(builder,
                       action,
                       item_id: int = None):
    data = action.split('-')
    callback = CALLBACK_DATA[data[0]](
        action=action
    )
    if item_id:
        callback.id = item_id
    builder.button(
        text='↩️',
        callback_data=callback
    )
    return builder
