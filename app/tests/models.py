from sqlalchemy import Column, Integer, String
from app.database import Base

class TestModel(Base):
    
    __tablename__ = "test_model" 

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    image_id = Column(Integer)