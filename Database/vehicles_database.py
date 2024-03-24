from .Database_Engine import Base

from sqlalchemy import Column, Integer, Float, String, Boolean, TIMESTAMP , BigInteger, UUID


class Vehicles_Table(Base):
    __tablename__ = "vehicles" 

    id = Column(UUID, 
                primary_key=True, 
                nullable=False)
    
    vehicle_type = Column(String, nullable=False)
    vehicle_make = Column(String, nullable=False)
    vehicle_model = Column(String, nullable=False)
    
    vehicle_reg_num = Column(String, nullable=False)
    vehicle_engine_cc = Column(Integer, nullable=False)
    vehicle_engine_num = Column(String, nullable=False) 
    vehicle_chassis_num = Column(String, nullable=False)
    
    vehicle_body_type = Column(String, nullable=False)
    
    vehicle_manufacture_year = Column(Integer, nullable=False)
    
    vehicle_origin_type = Column(String, nullable=False)
    
    vehicle_min_market_value = Column(Integer, nullable=True)
    vehicle_max_market_value = Column(Integer, nullable=True)

    created_by = Column(UUID, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    
    edited_by = Column(UUID, nullable=True)
    edited_at = Column(TIMESTAMP, nullable=True)
    
    
    
    