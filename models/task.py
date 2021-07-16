from typing import Any, Dict, List
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.query import Query
from models.base import Base
from const import message as msg
from flask_jwt_extended import get_jwt_identity
from flask_sqlalchemy_session import current_session

class Task(Base):
  __tablename__ = 'tasks'

  id = Column(Integer, primary_key=True)
  name = Column(String(50), nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  category_id = Column(Integer, ForeignKey('categories.id', ondelete="CASCADE"), nullable=False)
  memo = Column(String(100))
  notify_at = Column(DateTime)
  repeat_rate = Column(Integer, default=0)
  finished_at = Column(DateTime)
  # user = relationship("User", back_populates="tasks")
  # category = relationship("Category", back_populates="tasks")

  @classmethod
  def index(cls, category_id: int) -> 'List[Task]':
    query: Query = current_session.query(cls)
    tasks: List[Task] = query.filter(cls.category_id==category_id, cls.user_id==get_jwt_identity()).all()

    return tasks

  @classmethod
  def find_by_id(cls, task_id: int, query: Query=None) -> 'Task':
    if query == None:
      query = current_session.query(cls)

    return  query.filter(cls.id==task_id, cls.user_id==get_jwt_identity()).first()

  @classmethod
  def create(cls, body: Dict[str, str]) -> 'Task':
    notify_at = None if 'notify_at' not in body or body['notify_at'] == "" else body['notify_at']
    memo = "" if 'memo' not in body else body['memo']
    repeat_rate = None if 'repeat_rate' not in body or body['repeat_rate'] == "" else body['repeat_rate']
    
    task = cls(
      name=body['name'],
      category_id=body['category_id'],
      user_id=get_jwt_identity(),
      memo=memo,
      repeat_rate=repeat_rate,
      notify_at=notify_at
      )
    current_session.add(task)
    current_session.commit()

    return task

  @classmethod
  def update(cls,  task_id: int, body: Dict[str, str]) -> 'Task':
    task: 'Task' = Task.find_by_id(task_id)
    if task == None:
      return None
    for key, value in body.items():
      if key == 'id' or key == 'user_id':
        continue
      setattr(task, key, value)
    current_session.commit()

    return task

  @classmethod
  def delete(cls, task_id: int) -> str:
    task: Task = Task.find_by_id(task_id)
    if task == None:
      return None
    task_name = task.name
    current_session.delete(task)
    current_session.commit()
    
    return { "message": f"{ task_name }を削除しました" }

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "user_id": self.user_id,
      "category_id": self.category_id,
      "notify_at": self.notify_at,
      "repeat_rate": self.repeat_rate,
      "finished_at": self.finished_at
    }