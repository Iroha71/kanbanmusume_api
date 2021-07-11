from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  password = Column(String)
  token = Column(String)

  def to_dict(self):
      return { "id": self.id, "name": self.name }
    
  def to_dict_with_token(self):
    return { "id": self.id, "name": self.name, "token": self.token }