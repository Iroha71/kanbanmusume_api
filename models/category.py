from models.task import Task
from typing import Any, Dict, List
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from const import input_limit
from models.base import Base
class Category(Base):
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, nullable=False)
  name = Column(String(input_limit.CATEGORY_NAME), nullable=False)
  finish_rate = Column(Integer, default=0)
  # tasks = relationship("Task", back_populates="category")

  def to_dict(self) -> Dict[str, Any]:
    return {
      "id": self.id, 
      "name": self.name,
      "finished_rate": self.finish_rate
    }

  def create(self, current_session):
    current_session.add(self)
    current_session.commit()

  def update(self, name: str):
    self.name = name

    return self
