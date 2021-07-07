from werkzeug.security import safe_str_cmp
from typing import List
from flask_jwt import current_identity, jwt_required
from flask import Blueprint, request
from flask_restful import Resource, Api

app = Blueprint('auth', __name__)
api = Api(app)

class AuthLoginResource(Resource):
  @jwt_required()
  def get(self):
    """ 現在認証しているユーザ情報を返す（JWTのテスト用）
    """
    return f"{current_identity}"

api.add_resource(AuthLoginResource, '/auth/login')

class User(object):
  def __init__(self, id: int, username: str, password: str) -> None:
    self.id = id
    self.username = username
    self.password = password

  def __str__(self) -> str:
      return f"User(id={self.id}, password={self.password}, name={self.username}"

users = [
  User(1, 'user1', 'aaa'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username: str, password: str) -> User:
  """ パスワード認証を行い、ユーザ情報を返す

  Args:
      username (str): ユーザ名
      password (str): 入力されたパスワード

  Returns:
      User: 認証が成功したユーザ情報
  """
  user = username_table.get(username, None)
  if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
    return user

def identity(payload: List) -> User:
  """ IDを基にユーザ情報を返却する

  Args:
      payload (List): ユーザID

  Returns:
      User: ユーザIDが一致したユーザ情報
  """
  user_id = payload['identity']
  return userid_table.get(user_id, None)
