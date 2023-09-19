from app.crud.base import CRUDBase
from app.models.order import OrderItems


class CRUDOrderItems(CRUDBase):
    pass


order_items_crud = CRUDOrderItems(OrderItems)
