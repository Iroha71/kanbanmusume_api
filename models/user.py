from typing import Any, Dict
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  nickname = Column(String)
  password = Column(String)
  token = Column(String)

  def to_dict(self) -> Dict[str, Any]:
      return { "id": self.id, "name": self.name, "nickname": self.nickname }
    
  def to_dict_with_token(self) -> Dict[str, Any]:
    return { "id": self.id, "name": self.name, "nickname": self.nickname, "token": self.token }