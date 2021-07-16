from flask import Blueprint, request, jsonify
from typing import Any, Dict
from models.user import User
from const.message import NOT_FOUND, DUPLICATE_RECORD
from cerberus import Validator
from const import limit, message as msg
from flask_jwt_extended import jwt_required

app = Blueprint('user', __name__, url_prefix='/user')

v: Validator = Validator(allow_unknown=True)

@app.route('/', methods=['POST'])
def create():
  body = request.json.get('user')
  error_msgs: Dict[str, str] = limit.check_validate(v, rule=limit.USER, schemaname='user', req=body)
  if len(error_msgs) > 0:
    return jsonify(error_msgs), 422

  created_user_name: str = User.create(body)
  if created_user_name == None:
    return jsonify(DUPLICATE_RECORD['message']), DUPLICATE_RECORD['status']

  return jsonify({ "username": created_user_name })

@app.route('/<user_id>', methods=['PUT'])
@jwt_required()
def update(user_id: str) -> Dict[str, Any]:
  body = request.json.get('user')
  error_msgs: Dict[str, str] = limit.check_validate(v, rule=limit.UPDATE_USER, schemaname='user', req=body)
  if len(error_msgs) > 0:
    return jsonify(error_msgs), 422
    
  user: User = User.update(user_id, body)
  if user == None:
    return jsonify(NOT_FOUND['message']), NOT_FOUND['status']

  return jsonify(user.to_dict())

@app.route('/', methods=['GET'])
@jwt_required()
def find():
  user: User = User.find_by_id()
  if user == None:
    return jsonify(NOT_FOUND['message']), NOT_FOUND['status']

  return jsonify(user.to_dict())

@app.route('/regist_girl', methods=['POST'])
@jwt_required()
def regist_girl():
  girl_id: str = request.json.get('user')['girl_id']
  updated_user: User = User.regist_cur_girl(girl_id)
  if updated_user == None:
    return msg.NOT_FOUND['message'], msg.NOT_FOUND['status']
  
  return jsonify(updated_user.to_dict())