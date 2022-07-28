from sqlalchemy import String, Column, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Account(Base):
    __abstract__=True
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    login_at = Column(TIMESTAMP, nullable=True)
    
    def __init__(self,username=None,password=None,salt=None):
        self.username = username
        self.password =  password
        self.salt = salt
