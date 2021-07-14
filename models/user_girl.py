from typing import Any, Dict, List

from models.base import Base, convert_object2dict
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.query import Query

class UserGirl(Base):
  __tablename__ = 'user_girls'
  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
  girl_id = Column(Integer, ForeignKey('girls.id', ondelete='CASCADE'))
  level = Column(Integer, default=1)
  like_rate = Column(Integer, default=0)
  exp = Column(Integer, default=0)

  user = relationship("User", back_populates='girls')
  girl = relationship("Girl", back_populates='user_girls')

  @classmethod
  def index(cls, session, user_id: int) -> List[Dict[str, Any]]:
    query: Query = session.query(cls)
    girls: List['UserGirl'] = query.filter(cls.user_id==user_id).all()
    
    return convert_object2dict(girls)

  @classmethod
  def find_by_id(cls, session, user_girl_id: int) -> 'UserGirl':
    query: Query = session.query(cls)
    return query.filter(cls.id==user_girl_id).first()

  @classmethod
  def is_duplicate(cls, new_girl: 'UserGirl', session) -> bool:
    query: Query = session.query(cls)
    exist_record: int = len(query.filter(cls.user_id==new_girl.user_id, cls.girl_id==new_girl.girl_id).all())
    
    return exist_record > 0

  @classmethod
  def create(cls, session, user_id: int, girl_id: int) -> Dict[str, Any]:
    new_girl = cls(user_id=user_id, girl_id=girl_id)
    if cls.is_duplicate(new_girl, session):
      return None
    session.add(new_girl)
    session.commit()

    return new_girl.to_dict()

  @classmethod
  def update(cls, session, user_girl_id:int, body: Dict[str, Any]) -> Dict[str, Any]:
    girl: 'UserGirl' = cls.find_by_id(session, user_girl_id)
    if girl == None:
      return None
    
    for key, value in body.items():
      if key == 'girl_id' or key == 'user_id':
        continue
      setattr(girl, key, value)
    session.commit()

    return girl.to_dict()
  
  def to_dict(self):
    return {
      "id": self.id,
      "girl": self.girl.to_dict(),
      "level": self.level,
      "like_rate": self.like_rate,
      "exp": self.exp
    }
  