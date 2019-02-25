from sqlalchemy import Column, String
from db import Base

class Memo(Base):
    __tablename__ = 'Memo'

    memo_id = Column(String(20), primary_key=True)
    user_id = Column(String(20))
    title = Column(String(20))
    content = Column(String(100))