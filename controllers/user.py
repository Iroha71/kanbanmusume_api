from typing_extensions import Final
from flask import Blueprint, request, jsonify
from typing import Any, Dict
from const import input_limit
from models.user import User
from const.message import NOT_FOUND, DUPLICATE_RECORD

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

@app.route('/', methods=['POST'])
def create() -> Dict[str, Any]:
  body = request.json.get('user')
  created_user_name: str = User.create(body)
  if created_user_name == None:
    return jsonify(DUPLICATE_RECORD['message']), DUPLICATE_RECORD['status']

  return jsonify({ "username": created_user_name })

@app.route('/<user_id>', methods=['PUT'])
def update(user_id: str) -> Dict[str, Any]:
  body = request.json.get('user')
  user: User = User.update(user_id, body)
  if user == None:
    return jsonify(NOT_FOUND['message']), NOT_FOUND['status']

  return jsonify(user.to_dict())

@app.route('/<user_id>', methods=['GET'])
def find(user_id: str):
  user: User = User.find_by_id(user_id)
  if user == None:
    return jsonify(NOT_FOUND['message']), NOT_FOUND['status']

  return jsonify(user.to_dict())