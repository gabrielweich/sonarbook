import enum
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

SchemaType = TypeVar("SchemaType")


class Paginated(GenericModel, Generic[SchemaType]):
    total_items: int
    total_pages: int
    current_page: int
    items: List[SchemaType]


class OrderPage(enum.Enum):
    asc = "asc"
    desc = "desc"


class Sort(BaseModel):
    order_by: Optional[str] = None
    order: OrderPage
