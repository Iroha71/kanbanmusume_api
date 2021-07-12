from typing_extensions import Final
from flask import Blueprint, json, request, jsonify
from flask_sqlalchemy_session import current_session
from typing import Any, Dict, List
from const import input_limit
from models.user import User

app = Blueprint('user', __name__, url_prefix='/user')
USERNAME: Final[str] = "name"
NICKNAME: Final[str] = "nickname"
PASSWORD: Final[str] = "password"

def get_validate_errors(inputed_info: Dict[str, Any]) -> Dict[str, Any]:
  """入力されたユーザ情報が正しい規則になっているか確認する

  Args:
      inputed_info (Dict[str, Any]): 入力されたユーザ情報

  Returns:
      Dict[str, Any]: 入力規則違反の項目
  """
  limit = { USERNAME: input_limit.USERNAME, NICKNAME: input_limit.USER_NICKNAME, PASSWORD: input_limit.PASSWORD }
  errors_params = {}
  for key in inputed_info:
    if not key in limit:
      continue

    if len(inputed_info[key]) > limit[key] or inputed_info[key] == "":
      errors_params[key] = inputed_info[key]

  return errors_params

def check_duplicate_username(username: str) -> bool:
  """ユーザ名が重複しているか確認する

  Args:
      username (str): ユーザ名

  Returns:
      bool: ユーザ名が重複しているか
  """
  same_name_user: List[User] = current_session.query(User).filter(User.name == username).all()

  return len(same_name_user) > 0

@app.route('/', methods=['POST'])
def create() -> Dict[str, Any]:
  inputed_info = {
    USERNAME: request.json.get('name', None),
    NICKNAME: request.json.get('nickname', None),
    PASSWORD: request.json.get('password', None)
  }
  validate_errors: Dict[str, Any] = get_validate_errors(inputed_info)
  is_duplicate: bool = check_duplicate_username(inputed_info[USERNAME])
  if (len(validate_errors) > 0):
    return validate_errors
  if is_duplicate:
    return jsonify({"status": "ユーザ名が重複しています"})
  user = User(name=inputed_info[USERNAME], password=inputed_info[PASSWORD], nickname=inputed_info[NICKNAME])
  current_session.add(user)
  current_session.commit()

  return jsonify({ "status": "success" })

@app.route('/<user_id>', methods=['POST'])
def update(user_id: str) -> Dict[str, Any]:
  validate_errors = get_validate_errors(request.json)
  if len(validate_errors) > 0:
    return validate_errors
  
  user: User = current_session.query(User).filter(User.id == user_id).first()
  user.nickname = request.json.get('nickname', None)
  current_session.commit()

  return jsonify(user.to_dict())

@app.route('/<user_id>', methods=['GET'])
def find(user_id: str):
  user: User = current_session.query(User).filter(User.id == user_id).first()

  return jsonify(user.to_dict())