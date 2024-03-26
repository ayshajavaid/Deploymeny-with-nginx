
import pytz 
import hashlib
from datetime import datetime 

# Database
from sqlalchemy.orm import Session
from Database.Database_Engine import get_db

# UUID
import uuid


def Generate_Timestamp():
    """_summary_: Use this function to generate a timestamp
    Returns:
        _type_: str
    """
    # Choose your timezone
    timezone = pytz.timezone('UTC')  # You can replace 'UTC' with your desired timezone, like 'America/New_York'

    # Create a timezone-aware datetime
    now = datetime.now(timezone)

    # Convert to string if needed
    timestamp_str = now.isoformat()
    
    
    return timestamp_str


def HashPassword_SHA256(password:str):
    """_summary_: Use this function to hash a password using SHA256
    Args:
        password (str): Password to hash
    Returns:
        _type_: str
    """
    SHA256_Hash = hashlib.sha256(password.encode()).hexdigest()
    return SHA256_Hash

def Generate_UUID():
    """_summary_: Use this function to generate a UUID
    Returns:
        _type_: str
    """
    return str(uuid.uuid4())


# def Check_IF_User_Email_Already_Exists(email:str):
#     """_summary_: Use this function to check if a user already exists in the database
#     Args:
#         email (str): Email to check
#         cursor (cursor): Cursor to execute the query
#     Returns:
#         _type_: bool
#     """
#     cursor.execute("""SELECT * FROM user_credentials WHERE email = %s""", (email,))
#     user = cursor.fetchone()
#     if user:
#         return True
#     else:
#         return False
    
def check_Admin_User_Role_ID_Status(current_user):
    if current_user.role_id in [1, 2]:  # Only SuperAdmin:1 and Admin:2 are authorized
        return True
    else:
        return False
    
def check_General_User_Role_ID_Status(current_user):
    if current_user.role_id in [1, 2, 3]:  # Only SuperAdmin:1, Admin:2 and Employee:3 are authorized
        return True
    else:
        return False

def check_user_working_status(current_user):
    if current_user.working_status == True: # Only Active Users are authorized
        return True
    else:
        return False
        
    