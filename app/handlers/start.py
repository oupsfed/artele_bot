from aiogram import Router, types
from aiogram.filters import KICKED, ChatMemberUpdatedFilter, Command
from aiogram.types import ChatMemberUpdated
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import user_crud
from app.logger import logger
from app.models.user import Role

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message,
                    session: AsyncSession):
    telegram_user = message.chat
    user = await user_crud.get_by_attribute(
        'telegram_chat_id',
        telegram_user.id,
        session
    )
    if not user:
        user_data = {
            'telegram_chat_id': telegram_user.id,
            'first_name': telegram_user.first_name,
            'last_name': telegram_user.last_name,
            'username': telegram_user.username
        }
        user = await user_crud.create(
            user_data,
            session
        )
    text = 'Бот находится в стадии разработки'
    btn_text = 'Заказ'
    if user.role == Role.guest:
        btn_text = 'Заявка'
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Меню"),
        types.KeyboardButton(text='Корзина'),
    )
    builder.row(
        types.KeyboardButton(text=btn_text),
        types.KeyboardButton(text="Информация"),
    )
    if user.role == Role.guest:
        builder.row(
            types.KeyboardButton(text='Панель администратора'),
        )

    await message.answer(text,
                         parse_mode='HTML',
                         reply_markup=builder.as_markup(resize_keyboard=True))


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=KICKED)
)
async def user_blocked_bot(event: ChatMemberUpdated,
                           session: AsyncSession):
    logger.info(f'Пользователь {event.from_user.first_name} '
                f'{event.from_user.last_name} chat_id - {event.from_user.id}'
                f' заблокировал бота')
    user = await user_crud.get_by_attribute(
        'telegram_chat_id',
        event.from_user.id,
        session
    )
    await user_crud.remove(
        user,
        session
    )
