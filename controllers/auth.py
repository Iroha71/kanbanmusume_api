from werkzeug.security import safe_str_cmp
from models.user import User
from flask_sqlalchemy_session import current_session
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity

app = Blueprint('auth', __name__, url_prefix='/auth')

def current_user_id():
  return get_jwt_identity()

@app.route('/login', methods=['POST'])
def do_auth() -> User:
  """ユーザ認証を行う

  Returns:
      User: 認証に成功したユーザ情報
  """
  username = request.json.get('username', None)
  password = request.json.get('password', None)
  user: User = current_session.query(User).filter(User.name==username).first()
  user_id = user.id
  if user and safe_str_cmp(user.password, password):
    access_token = create_access_token(identity=user_id)

    return user.to_dict_with_token(access_token)
  else:
    return None