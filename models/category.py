from models.task import Task
from typing import Any, Dict, List, Union
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.base import Base
from flask_sqlalchemy_session import current_session
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.orm.query import Query
class Category(Base):
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, nullable=False)
  name = Column(String, nullable=False)
  finished_rate = Column(Integer, default=0)
  # tasks = relationship("Task", back_populates="category")

  @classmethod
  def index(cls) -> List['Category']:
    q: Query = current_session.query(cls)
    categories: List['Category'] = q.filter(cls.user_id==get_jwt_identity()).all()

    return categories

  @classmethod
  def find_by_id(cls, category_id: int, query: Query=None) -> 'Category':
    if query == None:
      query = current_session.query(cls)
    category: 'Category' = query.filter(cls.id==category_id, cls.user_id==get_jwt_identity()).first()
    
    return category

  @classmethod
  def create(cls, name: str) -> 'Category':
    category = cls(name=name, user_id=get_jwt_identity())
    current_session.add(category)
    current_session.commit()

    return category

  @classmethod
  def update(cls, id: int, name: str) -> 'Category':
    q: Query = current_session.query(cls)
    category: 'Category' = cls.find_by_id(id, q)
    if category == None:
      return None
    category.name = name
    current_session.commit()

    return category

  @classmethod
  def delete(cls, id: int) -> str:
    q: Query = current_session.query(cls)
    category: 'Category' = cls.find_by_id(id, q)
    if category == None:
      return None
    name = category.name
    current_session.delete(category)
    current_session.commit()

    return name

  def to_dict(self) -> Dict[str, Any]:
    return {
      "id": self.id, 
      "name": self.name,
      "finished_rate": self.finished_rate
    }
