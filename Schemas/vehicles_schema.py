
from enum import Enum
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


from uuid import UUID


### GET ALL Vehicles Response ###
class GET_All_Vehicles_Response(BaseModel):
    id: UUID
    
    vehicle_type: str
    vehicle_make: str
    vehicle_model: str
    
    vehicle_reg_num: str
    vehicle_engine_cc: int
    vehicle_engine_num: str
    vehicle_chassis_num: str
    
    vehicle_body_type: str
    
    vehicle_manufacture_year: int
    
    vehicle_origin_type: str
    
    vehicle_min_market_value: int
    vehicle_max_market_value: int
    
    created_by: UUID
    created_at: datetime
    
    # edited_by: Optional[str] = None
    # edited_at: Optional[datetime] = None
    
class Custom_GET_All_Vehicles_Pagination_Response(BaseModel):
    status: str
    message: str
    total_items: int
    page: int
    size: int
    data: list[GET_All_Vehicles_Response]

    class Config:
        from_attributes = True 


### GET Vehicles Filtered Response ###
class GET_Filtered_Vehicles_Response(BaseModel):
    id: UUID
    
    vehicle_type: str
    vehicle_make: str
    vehicle_model: str
    
    vehicle_reg_num: str
    vehicle_engine_cc: int
    vehicle_engine_num: str
    vehicle_chassis_num: str
    
    vehicle_body_type: str
    
    vehicle_manufacture_year: int
    
    vehicle_origin_type: str
    
    vehicle_min_market_value: int
    vehicle_max_market_value: int
    
    created_by: UUID
    created_at: datetime
    
    # edited_by: Optional[str] = None
    # edited_at: Optional[datetime] = None
    

    class Config:
        from_attributes = True


class Custom_Filtered_Vehicles_Pagination_Response(BaseModel):
    status: str
    message: str
    total_items: int
    page: int
    size: int
    data: list[GET_Filtered_Vehicles_Response]

    class Config:
        from_attributes = True 



### Get Single Vehicle by ID ###
class GET_Single_Vehicle_BY_ID_Response(BaseModel):
    id: UUID
    
    vehicle_type: str
    vehicle_make: str
    vehicle_model: str
    
    vehicle_reg_num: str
    vehicle_engine_cc: int
    vehicle_engine_num: str
    vehicle_chassis_num: str
    
    vehicle_body_type: str
    
    vehicle_manufacture_year: int
    
    vehicle_origin_type: str
    
    vehicle_min_market_value: int
    vehicle_max_market_value: int
    
    created_by: UUID
    created_at: datetime
    
class Custom_GET_Single_Vehicle_BY_ID_Response(BaseModel):
    status: str
    message: str
    
    # Fetching a single vehicle, the data field in Custom_GET_Single_Vehicle_BY_ID_Response 
    # should not be a list, but a single instance of GET_Single_Vehicle_BY_ID_Response.
    data: GET_Single_Vehicle_BY_ID_Response 
    
    # data: list[GET_Single_Vehicle_BY_ID_Response]

    class Config:
        from_attributes = True 
        

### Add Single Vehicle ###
class POST_Add_Single_Vehicle_Request(BaseModel):
    
    # id: str
    
    vehicle_type: str
    vehicle_make: str
    vehicle_model: str
    
    vehicle_reg_num: str
    vehicle_engine_cc: int
    vehicle_engine_num: str
    vehicle_chassis_num: str
    
    vehicle_body_type: str
    
    vehicle_manufacture_year: int
    
    vehicle_origin_type: str
    
    # vehicle_min_market_value: int
    # vehicle_max_market_value: int

    class Config:
        from_attributes = True


class Custom_POST_Add_Single_Vehicle_Response(BaseModel):
    status: str
    message: str

    class Config:
        from_attributes = True         



### Update Single Vehicle by ID ###
class PUT_Update_Single_Vehicle_BY_ID_Request(BaseModel):
    
    id: str
    
    vehicle_type: Optional[str] = None
    vehicle_make: Optional[str] = None
    vehicle_model: Optional[str] = None
    
    vehicle_reg_num: Optional[str] = None
    vehicle_engine_cc: Optional[int] = None
    vehicle_engine_num: Optional[str] = None
    vehicle_chassis_num: Optional[str] = None
    
    vehicle_body_type: Optional[str] = None
    
    vehicle_manufacture_year: Optional[int] = None
    
    vehicle_origin_type: Optional[str] = None
    
    vehicle_min_market_value: Optional[int] = None
    vehicle_max_market_value: Optional[int] = None

    class Config:
        from_attributes = True


class Custom_Update_Single_Vehicle_BY_ID_Request(BaseModel):
    status: str
    message: str

    class Config:
        from_attributes = True         


