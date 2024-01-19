from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):

    __tablename__ = "user_info"

    id = Column(String(length=255), primary_key=True)
    name = Column(String(length=255))
    flag = Column(String(length=255))

    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, flag={self.flag})'