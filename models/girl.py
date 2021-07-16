from typing import List
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql.sqltypes import Integer
from models.base import Base
from flask_sqlalchemy_session import current_session
from sqlalchemy.orm.query import Query

class Girl(Base):
  __tablename__ = 'girls'

  id = Column(Integer, primary_key=True)
  name = Column(String(30), nullable=False)
  code = Column(String(10), nullable=False, unique=True)
  detail = Column(String(100))
  birthday = Column(DateTime, nullable=False)
  
  @classmethod
  def index(cls) -> List['Girl']:
    query: Query = current_session.query(cls)
    girls: List['Girl'] = query.all()
    
    return girls

  @classmethod
  def find_by_id(cls, girl_id: int, query: Query=None) -> 'Girl':
    if query == None:
      query: Query = current_session.query(cls)
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