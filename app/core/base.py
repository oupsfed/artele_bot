"""Импорты класса Base и всех моделей для Alembic."""
from app.core.db import Base # noqa
from app.models.user import User # noqa
from app.models.item import Item # noqa
from app.models.cart import Cart # noqa
from app.models.order import OrderItems # noqa
from app.models.order import Order # noqa