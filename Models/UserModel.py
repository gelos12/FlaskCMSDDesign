from sqlalchemy import Column, String
from db import Base

class User(Base):
    __tablename__ = 'User'

    user_id = Column(String(20), primary_key=True)
    name = Column(String(20))
