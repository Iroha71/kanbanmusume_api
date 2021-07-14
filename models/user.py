from typing import Any, Dict
from sqlalchemy import Column, Integer, String
from models.base import Base
from sqlalchemy.orm import relationship

class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  nickname = Column(String)
  password = Column(String)

  girls = relationship("UserGirl", back_populates='user')
  # tasks = relationship("Task", back_populates="user")

  def to_dict(self) -> Dict[str, Any]:
      return { "id": self.id, "name": self.name, "nickname": self.nickname }
    
  def to_dict_with_token(self, token) -> Dict[str, Any]:
    info: Dict[str, Any] = self.to_dict()
    info['token'] = token
    
    return info