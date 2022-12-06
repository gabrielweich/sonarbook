import math
from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

import sqlalchemy as sa
from sqlalchemy import asc, desc, inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query

from src.db.mappings.base import BaseModel as BaseMapping
from src.services.exceptions.exceptions import AlreadyExistsError, ErrorCodeEnum
from src.services.models.base import BaseModel as BaseAppModel
from src.services.models.common import OrderPage, Paginated, Sort


AppModelType = TypeVar("AppModelType", bound=BaseAppModel)
MappingType = TypeVar("MappingType", bound=BaseMapping)


class BaseRepository(Generic[MappingType]):
    def __init__(self, db: AsyncSession, model: Type[MappingType]):
        self.db = db
        self.model = model

    def sort_query(
        self,
        query: Union[Query, sa.sql.Select],
        sort: Sort,
    ) -> Query:
        if sort is not None and sort.order_by is not None:
            sort_function = desc if sort.order == OrderPage.desc else asc
            order_by = sort.order_by
            if order_by in inspect(self.model).attrs.keys():
                order_by = getattr(self.model, order_by)
            sort_query = sort_function(order_by)
            query = query.order_by(sort_query)
        return query

    async def _paginate(self, select: Query, page: int, page_size: int):
        qb_count = sa.select(sa.func.count()).select_from(select.order_by(None))
        query_result = await self.db.execute(qb_count)
        total = query_result.scalars().first()
        paginated_qb = select.offset((page - 1) * page_size).limit(page_size)
        pages = int(math.ceil(total / float(page_size)))
        result = await self.db.execute(paginated_qb)
        return result, total, pages

    async def paginate_query(self, select: Query, model: Type[AppModelType], page: int, page_size: int):
        result, total, pages = await self._paginate(select, page, page_size)
        registers = result.unique().scalars().all()
        items = list(map(model.from_orm, registers))
        return Paginated(total_items=total, current_page=page, total_pages=pages, items=items)

    async def create(self, obj: MappingType) -> MappingType:
        try:
            self.db.add(obj)
            await self.db.flush([obj])
            return obj
        except sa.exc.IntegrityError as e:
            class_name = self.model.__name__
            raise AlreadyExistsError(
                code=ErrorCodeEnum.ALREADY_EXISTS, message=f"{class_name} already exists"
            ) from e

    async def update(self, id: Any, obj: Dict) -> MappingType:
        if obj:
            query = (
                sa.update(self.model)
                .where(self.model.id == id)
                .values(**obj)
                .execution_options(synchronize_session="fetch")
            )
            await self.db.execute(query)

        return await self.get_by_id(id)

    async def delete(self, id: Any):
        query = (
            sa.delete(self.model).where(self.model.id == id).execution_options(synchronize_session="fetch")
        )

        res = await self.db.execute(query)
        if res.rowcount == 1:
            return id
        return None

    async def get_by_id(self, id: Any) -> Optional[MappingType]:
        query = sa.select(self.model).where(self.model.id == id)
        res = await self.db.execute(query)
        return res.scalar()
