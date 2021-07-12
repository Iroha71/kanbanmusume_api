from _typeshed import Self
from typing import Any, Dict
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.query import Query
from const import input_limit
Base = declarative_base()
class Category(Base):
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, nullable=False)
  name = Column(String(input_limit.CATEGORY_NAME), nullable=False)
  finish_rate = Column(Integer, default=0)

  def to_dict(self) -> Dict[str, Any]:
    return {
      "id": self.id, 
      "name": self.name,
      "finished_rate": self.finish_rate
    }

  def create(self, current_session):
    current_session.add(self)
    current_session.commit()

  def update(current_session, name: str, user_id: int) -> Self:
    query: Query = current_session.query(Self)
    category: Self = query.filter(Self.user_id==user_id).first()
    category.name = name
    current_session.commit()
