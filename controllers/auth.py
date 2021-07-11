from werkzeug.security import safe_str_cmp
from typing import List
from models.user import User
from flask_sqlalchemy_session import current_session
from flask import Blueprint, request
from flask_jwt_extended import create_access_token

app = Blueprint('auth', __name__, url_prefix='/auth')

@app.route('/login', methods=['POST'])
def do_auth():
  username = request.json.get('username', None)
  password = request.json.get('password', None)
  user: User = current_session.query(User).filter(User.name==username).first()
  if password == user.password:
    access_token = create_access_token(identity=username)
    user.token = access_token
    current_session.commit()
    return user.to_dict_with_token()