from flask import request
from flask.json import jsonify
from models.user_girl import UserGirl
from typing import Any, Dict, List
from flask import Blueprint
from flask_jwt_extended import jwt_required
from const import message as msg

app = Blueprint('user_girl', __name__, url_prefix='/user_girl')

@app.route('/', methods=['GET'])
@jwt_required()
def index():
  have_girls: List[UserGirl] = UserGirl.index()
  if len(have_girls) <= 0:
    return jsonify(msg.NOT_FOUND['message']), msg.NOT_FOUND['status']
  res = [have_girl.to_dict() for have_girl in have_girls]

  return jsonify(res)

@app.route('/<user_girl_id>', methods=['GET'])
@jwt_required()
def find(user_girl_id: str):
  have_girl: UserGirl = UserGirl.find_by_id(user_girl_id)
  if have_girl == None:
    return jsonify(msg.NOT_FOUND['messsage']), msg.NOT_FOUND['status']

  return jsonify(have_girl.to_dict())

@app.route('/', methods=['POST'])
@jwt_required()
def create():
  girl_id: str = request.json.get('user_girl')['girl_id']
  new_girl: UserGirl = UserGirl.create(girl_id)
  if new_girl == None:
    return jsonify(msg.DUPLICATE_RECORD['message']), msg.DUPLICATE_RECORD['status']
  
  return jsonify(new_girl.to_dict())

@app.route('/<user_girl_id>', methods=['PUT'])
@jwt_required()
def update(user_girl_id: str):
  body: Dict[str, Any] = request.json.get('user_girl')
  updated_girl: UserGirl = UserGirl.update(user_girl_id, body)
  if updated_girl == None:
    return jsonify(msg.NOT_FOUND['message']), msg.NOT_FOUND['status']

  return jsonify(updated_girl.to_dict())