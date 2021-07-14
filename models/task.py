from typing import Any, Dict, List
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.query import Query
from models.base import Base, convert_object2dict
from const import message
from flask_jwt_extended import get_jwt_identity

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
  def index(cls, session, category_id: int) -> 'List[Task]':
    query: Query = session.query(cls)
    tasks: List[Task] = query.filter(cls.category_id==category_id, cls.user_id==get_jwt_identity()).all()
    res: Dict[str, Any] = convert_object2dict(tasks)

    return res

  @classmethod
  def create(cls, session, req: Dict[str, Any], category_id: int, current_user_id: int) -> Dict[str, Any]:
    notify_at = None if req['notify_at'] == "" else req['notify_at']
    
    task = cls(
      name=req['name'],
      category_id=category_id,
      user_id=current_user_id,
      memo=req['memo'],
      repeat_rate=req['repeat_rate'],
      notify_at=notify_at
      )
    session.add(task)
    session.commit()

    return task.to_dict()

  @classmethod
  def update(cls, session, body: Dict[str, Any], task_id: int, user_id) -> Dict[str, Any]:
    task = Task.find_by_id(session, task_id, user_id)
    for key, value in body.items():
      setattr(task, key, value)
    session.commit()

    return task.to_dict()

  @classmethod
  def delete(cls, session, task_id: int, user_id: int) -> str:
    task: Task = Task.find_by_id(session, task_id, user_id)
    if not Task.is_mine(task.user_id, user_id):
      return message.NOT_HAVE_ROLE_EDIT
    task_name = task.name
    session.delete(task)
    session.commit()
    
    return { "message": f"{ task_name }を削除しました" }

  @classmethod
  def find_by_id(cls, session, task_id: int, user_id: int) -> 'Task':
    query: Query = session.query(cls)
    return  query.filter(cls.id==task_id, cls.user_id==user_id).first()
  
  @classmethod
  def is_mine(cls, target_user_id, user_id: int) -> bool:
    print(target_user_id)
    print(user_id)
    return target_user_id == user_id

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