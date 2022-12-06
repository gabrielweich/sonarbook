from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import engine
from src.db.uow import UnitOfWork
from src.services.models.common import OrderPage, Sort


class PaginationParams:
    def __init__(
        self,
        page: int = 1,
        page_size: int = 15,
        order_by: str = None,
        order: OrderPage = OrderPage.asc,
    ):
        self.page = page
        self.page_size = page_size
        self.sort = Sort(order_by=order_by, order=order)


async def get_uow():
    session = AsyncSession(engine, expire_on_commit=True)
    try:
        yield UnitOfWork(session)
    finally:
        await session.close()
