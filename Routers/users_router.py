# FastAPI
from fastapi import Depends, status, Response, HTTPException, APIRouter

# Database
from sqlalchemy.orm import Session
from Database.Database_Engine import get_db

from Database import users_database

# Schema
from Schemas import users_schema


# My Functions
from Functions import oauth2, General_Func as GF


### Users Router ###
router = APIRouter(tags = ["Users"]) 

### Get All Users ###
@router.get("/users/all", 
            status_code=status.HTTP_200_OK,
            response_model=users_schema.Custom_GET_All_Users_Response,                   
            )
def get_all_users(
    response: Response, 
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.Get_Current_User)
    ):
    try:
        user_ID_status = GF.check_Admin_User_Role_ID_Status(current_user) # Check if the User ID is valid
        user_working_status = GF.check_user_working_status(current_user) # Check if the User is working
        
        if (user_ID_status == True) and (user_working_status == True):
            users_query = db.query(users_database.Users_Table).all()
            return {'status': 'success', 
                    'message': 'Data Fetched Successfully', 
                    'data': users_query}

        
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


### Add Single Users ###
@router.post("/users/add", 
            status_code=status.HTTP_200_OK,
            response_model=users_schema.Custom_POST_Add_Single_User_Response,                   
            )
def add_single_users(
    POST_request_body: users_schema.POST_Add_Single_User_Request,
    response: Response, 
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.Get_Current_User)
    ):
    try:
        user_ID_status = GF.check_Admin_User_Role_ID_Status(current_user) # Check if the User ID is valid
        user_working_status = GF.check_user_working_status(current_user) # Check if the User is working
        
        if (user_ID_status == True) and (user_working_status == True):
            # Check if the User already exists
            user_data = db.query(users_database.Users_Table).filter(users_database.Users_Table.email == POST_request_body.email).first()
            
            if user_data is not None: # If User Already Exists
                response.status_code = status.HTTP_409_CONFLICT
                return {'status': 'error',
                        'message': 'User Already Exists'
                        }
            
            else:
                           
                user_data = users_database.Users_Table(
                    user_id = GF.Generate_UUID(),
                    email = POST_request_body.email,
                    first_name = POST_request_body.first_name,
                    last_name = POST_request_body.last_name,
                    password = GF.HashPassword_SHA256(POST_request_body.password),
                    role = POST_request_body.role,
                    working_status = POST_request_body.working_status,
                    created_at=GF.Generate_Timestamp()
                )
            
                db.add(user_data) # Add to the Database
                db.commit() # Commit to the Database
                db.refresh(user_data) # Refresh the Database
                
                return {'status': 'success', 
                        'message': 'User Added Successfully'
                        }
                
        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {'status': 'error',
                    'message': 'Unauthorized Access',
                    }

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(f'Error Adding User: {e}')
        return {'status': 'error',
                'message': 'User Not Added Successfully'
                }
        
        
        
### Update Single Users ###
@router.put("/users/update", 
            status_code=status.HTTP_200_OK,
            response_model=users_schema.Custom_PUT_Update_Single_User_Response)
def update_single_user(
    PUT_request_body: users_schema.PUT_Update_Single_User_Request,
    response: Response, 
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.Get_Current_User)
):
    try:
        user_ID_status = GF.check_Admin_User_Role_ID_Status(current_user)
        user_working_status = GF.check_user_working_status(current_user)

        if (user_ID_status == True) and (user_working_status == True):
            # Find the User to update
            user_data = db.query(users_database.Users_Table).filter(users_database.Users_Table.email == PUT_request_body.email).first()

            if user_data is None:
                response.status_code = status.HTTP_404_NOT_FOUND
                return {'status': 'error',
                        'message': 'User Not Found'}
            
            else:
                # Update user details if provided
                if PUT_request_body.first_name is not None:
                    user_data.first_name = PUT_request_body.first_name
                if PUT_request_body.last_name is not None:
                    user_data.last_name = PUT_request_body.last_name
                if PUT_request_body.role is not None:
                    user_data.role = PUT_request_body.role
                if PUT_request_body.working_status is not None:
                    user_data.working_status = PUT_request_body.working_status


                db.commit()
                db.refresh(user_data)

                return {'status': 'success', 
                        'message': 'User Updated Successfully'}
            
        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {'status': 'error',
                    'message': 'Unauthorized Access'}

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(f'Error Updating User: {e}')
        return {'status': 'error',
                'message': 'User Not Updated Successfully'}

        
        
### Delete Single Users ###
@router.delete("/users/delete", 
            status_code=status.HTTP_200_OK,
            response_model=users_schema.Custom_DELETE_Single_User_Response,                   
            )
def delete_single_users(
    DELETE_request_body: users_schema.DELETE_Single_User_Request,
    response: Response, 
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.Get_Current_User)
    ):
    try:
        user_ID_status = GF.check_Admin_User_Role_ID_Status(current_user) # Check if the User ID is valid
        user_working_status = GF.check_user_working_status(current_user) # Check if the User is working
        
        if (user_ID_status == True) and (user_working_status == True):
            # Check if the User exists
            user_data = db.query(users_database.Users_Table).filter(users_database.Users_Table.email == DELETE_request_body.email).first()
            
            if user_data is None: # If User Not Found
                response.status_code = status.HTTP_404_NOT_FOUND
                return {'status': 'error',
                        'message': 'User Not Found'
                        }
            else:
                db.delete(user_data) # Delete from the Database
                db.commit() # Commit to the Database
            
            return {'status': 'success', 
                    'message': 'User Deleted Successfully'
                    }
        
        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {'status': 'error',
                    'message': 'Unauthorized Access',
                    }
           

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(f'Error Adding User: {e}')
        return {'status': 'error',
                'message': 'User Not Deleted Successfully'
                }
