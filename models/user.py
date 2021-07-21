from sqlalchemy.sql.expression import join
from models.user_girl import UserGirl
from models.girl import Girl
from typing import Any, Dict, List, Union
from flask_jwt_extended.utils import get_jwt_identity
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from models.base import Base, get_query
from sqlalchemy.orm import base, relationship
from flask_sqlalchemy_session import current_session
from sqlalchemy.orm.query import Query
from models import user_girl as ug
class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  nickname = Column(String)
  password = Column(String)
  coin = Column(Integer, default=0)
  line_id = Column(String)

  user_girls = relationship('UserGirl', back_populates='owner_user')
  cur_partner = None
  
  @classmethod
  def find_by_id(cls, query: Query=None) -> Any:
    if query == None:
      query = current_session.query(cls)
    user: 'User' = query.filter(cls.id==get_jwt_identity()).first()
    for unlocked_girl in user.user_girls:
      if unlocked_girl.is_partner == ug.IS_PARTNER:
        user.cur_partner = unlocked_girl
        break
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
  def update(cls, body: Dict[str, Any]) -> 'User':
    user: Any = cls.find_by_id()
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
  
  def add_coin(self, gave_coin: int):
    self.coin += gave_coin
    if (self.coin < 0):
      self.coin = 0

  def to_dict(self):
    return {
      "id": self.name,
      "name": self.name,
      "nickname": self.nickname,
      "coin": self.coin,
      "partner": self.cur_partner.to_dict()
    }