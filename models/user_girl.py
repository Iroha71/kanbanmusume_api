from typing import Any, Dict, List
from flask_sqlalchemy_session import current_session
from flask_jwt_extended import get_jwt_identity
from models.base import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.query import Query
from const.limit import DONE_TASK_EXP, REQUIRE_EXP_BASE, REQUIRE_EXP_MULTIPLE

class UserGirl(Base):
  __tablename__ = 'user_girls'
  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
  girl_id = Column(Integer, ForeignKey('girls.id', ondelete='CASCADE'))
  level = Column(Integer, default=1)
  like_rate = Column(Integer, default=0)
  exp = Column(Integer, default=0)
  require_exp = Column(Integer, default=REQUIRE_EXP_BASE)

  # girl = relationship("Girl", backref='user_girls')

  @classmethod
  def index(cls) -> List['UserGirl']:
    query: Query = current_session.query(cls)
    girls: List['UserGirl'] = query.filter(cls.user_id==get_jwt_identity()).all()

    return girls

  @classmethod
  def find_by_id(cls, user_girl_id: int, query: Query=None) -> 'UserGirl':
    if query == None:
      query = current_session.query(cls)
    user_girl: 'UserGirl' = query.filter(cls.user_id==get_jwt_identity(), cls.id==user_girl_id).first()

    return user_girl

  @classmethod
  def create(cls, girl_id: int) -> 'UserGirl':
    new_girl = cls(user_id=get_jwt_identity(), girl_id=girl_id)
    if cls.is_duplicate(new_girl):
      return None
    current_session.add(new_girl)
    current_session.commit()

    return new_girl

  @classmethod
  def update(cls, user_girl_id:int, body: Dict[str, Any]) -> 'UserGirl':
    girl: 'UserGirl' = cls.find_by_id(user_girl_id)
    if girl == None:
      return None
    
    for key, value in body.items():
      if key == 'girl_id' or key == 'user_id':
        continue
      setattr(girl, key, value)
    current_session.commit()

    return girl

  @classmethod
  def is_duplicate(cls, new_girl: 'UserGirl') -> bool:
    query: Query = current_session.query(cls)
    exist_record: int = len(query.filter(cls.user_id==new_girl.user_id, cls.girl_id==new_girl.girl_id).all())
    
    return exist_record > 0
  
  @classmethod
  def change_girl(cls, new_girl_id: int, old_girl_id: int, query: Query=None) -> 'UserGirl':
    if query == None:
      query = current_session.query(cls)
    new_cur_girl: 'UserGirl' = query.filter(cls.user_id==get_jwt_identity(), cls.girl_id==new_girl_id).first()
    new_cur_girl.is_partner = 1
    changed_girl: 'UserGirl' = query.filter(cls.user_id==get_jwt_identity(), cls.girl_id==old_girl_id).first()
    changed_girl.is_partner = 0
    current_session.commit()

  def add_exp(self, done_task_num: int):
    add_exp = done_task_num * DONE_TASK_EXP
    self.exp += add_exp
    if (self.exp >= self.require_exp):
      self = self.up_level()
    current_session.commit()

  def up_level(self) -> 'UserGirl':
    self.level += 1
    self.exp = 0
    self.require_exp *= REQUIRE_EXP_MULTIPLE

    return self
  
  def to_dict(self):
    return {
      "id": self.id,
      "girl": self.girl.to_dict(),
      "level": self.level,
      "like_rate": self.like_rate,
      "exp": self.exp
    }
  