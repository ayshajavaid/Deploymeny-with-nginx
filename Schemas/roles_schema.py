from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GET_All_Roles_Response(BaseModel):
    role_id: int
    role_type: str

    class Config:
        from_attributes = True


class Custom_GET_All_Roles_Response(BaseModel):
    status: str
    message: str
    data: list[GET_All_Roles_Response]

    class Config:
        from_attributes = True 
