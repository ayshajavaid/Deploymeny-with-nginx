from pydantic import BaseModel
from typing import Optional
from datetime import datetime

### Users GET Response ###
class GET_All_Users_Response(BaseModel):
    # id: int
    
    email: str
    
    first_name: str
    last_name: str
    
    # password: str
    # role: int
    # working_status: bool
    
    created_at: datetime

    class Config:
        from_attributes = True


class Custom_GET_All_Users_Response(BaseModel):
    status: str
    message: str
    data: list[GET_All_Users_Response]

    class Config:
        from_attributes = True 



### Add Single User ###
class POST_Add_Single_User_Request(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str
    role: int
    working_status: bool


    class Config:
        from_attributes = True
        
class Custom_POST_Add_Single_User_Response(BaseModel):
    status: str
    message: str

    class Config:
        from_attributes = True
        
        
### Update Single User ###
class PUT_Update_Single_User_Request(BaseModel):
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    # password: Optional[str]
    role: Optional[int]
    working_status: Optional[bool]

    class Config:
        from_attributes = True

class Custom_PUT_Update_Single_User_Response(BaseModel):
    status: str
    message: str

    class Config:
        from_attributes = True

### Delete Single User ###
class DELETE_Single_User_Request(BaseModel):
    email: str

    class Config:
        from_attributes = True

class Custom_DELETE_Single_User_Response(BaseModel):
    status: str
    message: str

    class Config:
        from_attributes = True
        
