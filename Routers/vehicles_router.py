

from uuid import UUID

# FastAPI
from fastapi import Depends, Query, status, Response, APIRouter
from pydantic import BaseModel

# OAuth2
from Functions import oauth2

# Database
from sqlalchemy import select, or_, and_, desc, asc, func
from sqlalchemy.orm import Session
from Database.Database_Engine import get_db
from Database import vehicles_database, users_database

# Schema
from Schemas import vehicles_schema

# My Functions
from Functions import General_Func as GF
from Functions.Pagination_Func import pagination_params, SortEnum, Pagination




### Vehicles Router ###
router = APIRouter(tags=["Vehicles"]) # tags=["Roles"], prefix="/roles"


### Get All Vehicles with Pagination ###
@router.get("/vehicles/all", 
            status_code=status.HTTP_200_OK,
            response_model=vehicles_schema.Custom_GET_All_Vehicles_Pagination_Response,                    
            )
def get_all_vehicles(
    response: Response,
    pagination: Pagination = Depends(pagination_params),
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.Get_Current_User)
    ):
    
    try:
        user_ID_status = GF.check_Admin_User_Role_ID_Status(current_user) # Check if the User ID is valid
        user_working_status = GF.check_user_working_status(current_user) # Check if the User is working

        if (user_ID_status == True) and (user_working_status == True):
            
            order_function = desc if pagination.order == SortEnum.DESC else asc
            offset_value = (pagination.page - 1) * pagination.perPage
            
            # Get Total Items Query
            total_items_query = (
                select(func.count())
                .select_from(vehicles_database.Vehicles_Table)
            )
            total_items = db.execute(total_items_query).scalar()
            
            if total_items == 0: # If there are no items in the Database
                return {'status': 'success',
                        'message': 'No Vehicles Data Available',
                        'total_items': 0,
                        'page': 0,
                        'size': 0,
                        'data': []
                        }
            
            else:
                vehicles_query = (
                    select(vehicles_database.Vehicles_Table)
                    .limit(pagination.perPage)
                    .offset(offset_value)
                    .order_by(order_function(vehicles_database.Vehicles_Table.created_at))
                )
                vehicles = db.execute(vehicles_query).scalars().all()

                return {
                    'status': 'success',
                    'message': 'Vehicles Data Retrieved Successfully',
                    'total_items': total_items,
                    'page': pagination.page,
                    'size': pagination.perPage,
                    'data': vehicles
                    }            
        
        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {'status': 'error', 
                    'message': 'Unauthorized Access',
                    'total_items': 0,
                    'page': 0,
                    'size': 0, 
                    'data': []
                    }
        
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        # print(f'Error Retrieving Vehicles: {e}')
        return {'status': 'error', 
                'message': 'Vehicles Data Not Retrieved Successfully', 
                'total_items': 0,
                'page': 0,
                'size': 0, 
                'data': []
                }





### Get All Filtered Vehicles with Pagination ###
@router.get("/vehicles/filtered", 
            status_code=status.HTTP_200_OK,
            response_model=vehicles_schema.Custom_Filtered_Vehicles_Pagination_Response,                    
            )
def get_filtered_vehicles(
    response: Response,
    pagination: Pagination = Depends(pagination_params),
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.Get_Current_User)
    ):
    
    try:
        user_ID_status = GF.check_General_User_Role_ID_Status(current_user) # Check if the User ID is valid
        user_working_status = GF.check_user_working_status(current_user) # Check if the User is working

        if (user_ID_status == True) and (user_working_status == True):
            
            order_function = desc if pagination.order == SortEnum.DESC else asc
            offset_value = (pagination.page - 1) * pagination.perPage
            
            # Get Total Items Query
            total_items_query = (
                select(func.count())
                .select_from(vehicles_database.Vehicles_Table)
            )
            total_items = db.execute(total_items_query).scalar()
            
            if total_items == 0: # If there are no items in the Database
                return {'status': 'success',
                        'message': 'No Vehicles Data Available',
                        'total_items': 0,
                        'page': 0,
                        'size': 0,
                        'data': []
                        }
            
            else:
                # Filtered query: Get All Vehicles with Market Value = 0
                vehicles_query = select(vehicles_database.Vehicles_Table).where(
                    vehicles_database.Vehicles_Table.vehicle_min_market_value == 0,
                    vehicles_database.Vehicles_Table.vehicle_max_market_value == 0
                )
                
                vehicles_query = (
                    select(vehicles_database.Vehicles_Table)
                    .limit(pagination.perPage)
                    .offset(offset_value)
                    .order_by(order_function(vehicles_database.Vehicles_Table.created_at))
                )
                vehicles = db.execute(vehicles_query).scalars().all()

                return {
                    'status': 'success',
                    'message': 'Vehicles Data Retrieved Successfully',
                    'total_items': total_items,
                    'page': pagination.page,
                    'size': pagination.perPage,
                    'data': vehicles
                    }            
        
        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {'status': 'error', 
                    'message': 'Unauthorized Access',
                    'total_items': 0,
                    'page': 0,
                    'size': 0, 
                    'data': []
                    }
        
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        # print(f'Error Retrieving Vehicles: {e}')
        return {'status': 'error', 
                'message': 'Vehicles Data Not Retrieved Successfully', 
                'total_items': 0,
                'page': 0,
                'size': 0, 
                'data': []
                }


### GET Single Vehicle by ID ###
@router.get("/vehicles/{vehicle_id}", 
            status_code=status.HTTP_200_OK,
            response_model=vehicles_schema.Custom_GET_Single_Vehicle_BY_ID_Response
            )
def get_vehicle_by_id(
    vehicle_id: UUID,
    response: Response, 
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.Get_Current_User)
    ):
    try:
        user_ID_status = GF.check_General_User_Role_ID_Status(current_user) # Check if the User ID is valid
        user_working_status = GF.check_user_working_status(current_user) # Check if the User is working

        if (user_ID_status == True) and (user_working_status == True):
            
            vehicle_query = select(vehicles_database.Vehicles_Table).where(
            vehicles_database.Vehicles_Table.id == vehicle_id)
            
            
            vehicle = db.execute(vehicle_query).scalars().first()
            
            if vehicle == None:
                response.status_code = status.HTTP_404_NOT_FOUND
                return {'status': 'error',
                        'message': 'Vehicle Data Not Found',
                        'data': []
                        }
                
            else:
                return {'status': 'success',
                        'message': 'Vehicle Data Retrieved Successfully',
                        'data': vehicle
                        }
            
        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {'status': 'error', 
                    'message': 'Unauthorized Access',
                    'data': []
                    }
            
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        # print(f'Error Retrieving Vehicles: {e}')
        return {'status': 'error', 
                'message': 'Vehicle Data Not Retrieved Successfully', 
                'data': []
                }




### Add Single Vehicles ###
@router.post("/vehicles/add", 
            status_code=status.HTTP_200_OK,
            response_model=vehicles_schema.Custom_POST_Add_Single_Vehicle_Response,                   
            )
def add_single_users(
    POST_request_body: vehicles_schema.POST_Add_Single_Vehicle_Request,
    response: Response, 
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.Get_Current_User)
    ):
    try:
        user_ID_status = GF.check_General_User_Role_ID_Status(current_user) # Check if the User ID is valid
        user_working_status = GF.check_user_working_status(current_user) # Check if the User is working
        
        if (user_ID_status == True) and (user_working_status == True):
            
            current_user_UUID = db.query(users_database.Users_Table).filter(users_database.Users_Table.email == current_user.user_email).first()
            current_user_UUID = current_user_UUID.user_id
            
            vehicle_data = vehicles_database.Vehicles_Table(
                id = GF.Generate_UUID(),
                vehicle_type = (POST_request_body.vehicle_type).lower(),
                vehicle_make = (POST_request_body.vehicle_make).lower(),
                vehicle_model = (POST_request_body.vehicle_model).lower(),
                
                vehicle_reg_num = (POST_request_body.vehicle_reg_num).lower(),
                vehicle_engine_cc = POST_request_body.vehicle_engine_cc,
                vehicle_engine_num = (POST_request_body.vehicle_engine_num).lower(),
                vehicle_chassis_num = (POST_request_body.vehicle_chassis_num).lower(),
                
                vehicle_body_type = (POST_request_body.vehicle_body_type).lower(),
                
                vehicle_manufacture_year = POST_request_body.vehicle_manufacture_year,
                
                vehicle_origin_type = (POST_request_body.vehicle_origin_type).lower(),
                
                vehicle_min_market_value = 0,
                vehicle_max_market_value = 0,
                
                created_by = current_user_UUID,
                created_at=GF.Generate_Timestamp()
            )
             
            db.add(vehicle_data) # Add to the Database
            db.commit() # Commit to the Database
            db.refresh(vehicle_data) # Refresh the Database
            
            return {'status': 'success', 
                    'message': 'Vehicle Added Successfully'
                    }
                
        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {'status': 'error',
                    'message': 'Unauthorized Access',
                    }

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        # print(f'Error Adding User: {e}')
        return {'status': 'error',
                'message': 'Vehicle Not Added Successfully'
                }

    


### Update Single Vehicle by ID ###
@router.put("/vehicles/update", 
            status_code=status.HTTP_200_OK,
            response_model=vehicles_schema.Custom_Update_Single_Vehicle_BY_ID_Request
            )
def update_vehicle_by_id(
    PUT_request_body: vehicles_schema.PUT_Update_Single_Vehicle_BY_ID_Request,
    response: Response, 
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.Get_Current_User)    
):
    try:
        user_ID_status = GF.check_General_User_Role_ID_Status(current_user) # Check if the User ID is valid
        user_working_status = GF.check_user_working_status(current_user) # Check if the User is working
        
        if (user_ID_status == True) and (user_working_status == True):
            
            # Find the Vehicle to update
            vehicle_data = db.query(vehicles_database.Vehicles_Table).filter(vehicles_database.Vehicles_Table.id == PUT_request_body.id).first()

            if vehicle_data is None:
                response.status_code = status.HTTP_404_NOT_FOUND
                return {'status': 'error',
                        'message': 'User Not Found'}
                
            else:
                current_user_UUID = db.query(users_database.Users_Table).filter(users_database.Users_Table.email == current_user.user_email).first()
                current_user_UUID = current_user_UUID.user_id
                
                # Update vehicle details if provided
                if PUT_request_body.vehicle_type is not None:
                    vehicle_data.vehicle_type = (PUT_request_body.vehicle_type).lower()
                
                if PUT_request_body.vehicle_make is not None:
                    vehicle_data.vehicle_make = (PUT_request_body.vehicle_make).lower()

                if PUT_request_body.vehicle_model is not None:
                    vehicle_data.vehicle_model = (PUT_request_body.vehicle_model).lower()
                    
                if PUT_request_body.vehicle_reg_num is not None:
                    vehicle_data.vehicle_reg_num = (PUT_request_body.vehicle_reg_num).lower()

                if PUT_request_body.vehicle_engine_cc is not None:
                    vehicle_data.vehicle_engine_cc = PUT_request_body.vehicle_engine_cc
                
                if PUT_request_body.vehicle_engine_num is not None:
                    vehicle_data.vehicle_engine_num = (PUT_request_body.vehicle_engine_num).lower()
                
                if PUT_request_body.vehicle_chassis_num is not None:
                    vehicle_data.vehicle_chassis_num = (PUT_request_body.vehicle_chassis_num).lower()
                
                if PUT_request_body.vehicle_body_type is not None:
                    vehicle_data.vehicle_body_type = (PUT_request_body.vehicle_body_type).lower()
                
                if PUT_request_body.vehicle_manufacture_year is not None:
                    vehicle_data.vehicle_manufacture_year = PUT_request_body.vehicle_manufacture_year
                
                if PUT_request_body.vehicle_origin_type is not None:
                    vehicle_data.vehicle_origin_type = (PUT_request_body.vehicle_origin_type).lower()

                if PUT_request_body.vehicle_min_market_value is not None:
                    vehicle_data.vehicle_min_market_value = PUT_request_body.vehicle_min_market_value
                    
                if PUT_request_body.vehicle_max_market_value is not None:
                    vehicle_data.vehicle_max_market_value = PUT_request_body.vehicle_max_market_value
                    
                vehicle_data.edited_by = current_user_UUID
                vehicle_data.edited_at = GF.Generate_Timestamp()
                
                
                db.commit()
                db.refresh(vehicle_data)

                return {'status': 'success', 
                        'message': 'User Updated Successfully'}
        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {'status': 'error',
                    'message': 'Unauthorized Access'
                    }
            
        
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        # print(f'Error Updating Vehicle: {e}')
        return {'status': 'error',
                'message': 'Vehicle Not Updated Successfully'
                }
    