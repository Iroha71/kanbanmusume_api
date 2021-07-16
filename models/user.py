from typing import Any, Dict, List, Union
from sqlalchemy import Column, Integer, String
from models.base import Base
from sqlalchemy.orm import relationship
from flask_sqlalchemy_session import current_session
from sqlalchemy.orm.query import Query
class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  nickname = Column(String)
  password = Column(String)

  girls = relationship("UserGirl", back_populates='user')
  # tasks = relationship("Task", back_populates="user")
  
  @classmethod
  def find_by_id(cls, id: int, query: Query=None) -> 'User':
    if query == None:
      query = current_session.query(cls)
    user: 'User' = query.filter(cls.id==id).first()
    if user == None:
      return None
    
    return user
  
  @classmethod
  def create(cls, body: Dict[str, Any]) -> str:
    if cls.is_duplicate_name(body['name']):
      return None
    new_user = cls(
      name=body['name'],
      nickname=body['nickname'],
      password=body['password']
    )
    current_session.add(new_user)
    current_session.commit()

    return new_user.name

  @classmethod
  def update(cls, id: int, body: Dict[str, Any]) -> 'User':
    user: 'User' = cls.find_by_id(id)
    if user == None:
      return None
    for key, value in body.items():
      if key == 'name' or key == 'id':
        continue
      setattr(user, key, value)
    current_session.commit()

    return user

  @classmethod
  def is_duplicate_name(cls, name: str) -> bool:
    """ユーザ名が重複しているか

    Args:
        name (str): 登録予定のユーザ名

    Returns:
        bool: ユーザ名が重複しているか
    """
    query: Query = current_session.query(cls)
    same_name_user: List['User'] = query.filter(cls.name==name).all()

    return len(same_name_user) > 0

  def to_dict(self, token: str=None) -> Dict[str, Any]:
      info: Dict[str, Union[str, int]] = {
        "id": self.id,
        "name": self.name,
        "nickname": self.nickname
      }
      if token != None:
        info['token'] = token
      return info