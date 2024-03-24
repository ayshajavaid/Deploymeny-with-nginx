
# FastAPI
from fastapi import Depends, status, Response, APIRouter

# OAuth2
from Functions import oauth2

# Database
from sqlalchemy.orm import Session
from Database.Database_Engine import get_db
from Database import roles_database

# Schema
from Schemas import roles_schema

# My Functions
from Functions import General_Func as GF


### Blog Router ###
router = APIRouter(tags = ["Roles"]) 

### Get All Roles ###
@router.get("/roles/all", 
            status_code=status.HTTP_200_OK,
            response_model=roles_schema.Custom_GET_All_Roles_Response,                   
            )
def get_all_roles(
    response: Response, 
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.Get_Current_User)
    ):
    try:
        user_ID_status = GF.check_Admin_User_Role_ID_Status(current_user) # Check if the User ID is valid
        user_working_status = GF.check_user_working_status(current_user) # Check if the User is working
        
        if (user_ID_status == True) and (user_working_status == True):
            roles_query = db.query(roles_database.Roles_Table).all()
            return {'status': 'success', 
                    'message': 'Data Fetched Successfully', 
                    'data': roles_query}

        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {'status': 'error',
                    'message': 'Unauthorized Access',
                    'data': []}


    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'status': 'error',
                'message': 'Data Not Fetched',
                'data': []}
        