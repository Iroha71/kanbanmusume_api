from typing import Any, Dict, List
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer
from models.base import Base, convert_object2dict
from sqlalchemy.orm.query import Query

class Girl(Base):
  __tablename__ = 'girls'

  id = Column(Integer, primary_key=True)
  name = Column(String(30), nullable=False)
  code = Column(String(10), nullable=False, unique=True)
  detail = Column(String(100))
  birthday = Column(DateTime, nullable=False)

  user_girls = relationship('UserGirl', back_populates='girl')

  @classmethod
  def index(cls, session) -> List[Dict[str, Any]]:
    query: Query = session.query(cls)
    girls: List['Girl'] = query.all()
    
    return convert_object2dict(girls)

  @classmethod
  def find_by_id(cls, session, girl_id: int) -> 'Girl':
    query: Query = session.query(cls)
    girl: 'Girl' = query.filter(cls.id==girl_id).first()

    return girl

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "code": self.code,
      "detail": self.detail,
      "birthday": self.birthday
    }