from enum import Enum

# FastAPI
from pydantic import BaseModel
from fastapi import Query


class SortEnum(str, Enum):
    ASC = "asc"
    DESC = "desc"
    
class Pagination(BaseModel):
    page: int
    perPage: int
    order: SortEnum

def pagination_params(
    page: int = Query(ge=1, description="Page number", default=1),
    perPage: int = Query(ge=1, le=100, description="Items per page", default=10),
    order: SortEnum = Query(default=SortEnum.DESC, description="Sorting order"),            
    ):
    return Pagination(perPage=perPage, page=page, order=order.value)
