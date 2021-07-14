from flask import request
from flask.json import jsonify
from models.user_girl import UserGirl
from typing import Any, Dict, List
from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_sqlalchemy_session import current_session
from const import message

app = Blueprint('user_girl', __name__, url_prefix='/user_girl')

@app.route('/', methods=['GET'])
@jwt_required()
def index():
  have_girls: List[Dict[str, Any]] = UserGirl.index(current_session, get_jwt_identity())

  return jsonify(have_girls)

@app.route('/<user_girl_id>', methods=['GET'])
@jwt_required()
def find(user_girl_id: str):
  have_girl: UserGirl = UserGirl.find_by_id(current_session, user_girl_id)
  if have_girl == None:
    return jsonify({})

  return jsonify(have_girl.to_dict())

@app.route('/', methods=['POST'])
@jwt_required()
def create():
  user_id: str = request.json.get('user_girl')['user_id']
  girl_id: str = request.json.get('user_girl')['girl_id']
  new_girl: Dict[str, Any] = UserGirl.create(current_session, user_id, girl_id)
  if new_girl == None:
    return jsonify(message.DUPLICATE_RECORD)
  return jsonify(new_girl)

@app.route('/<user_girl_id>', methods=['PUT'])
@jwt_required()
def update(user_girl_id: str):
  body: Dict[str, Any] = request.json.get('user_girl')
  updateed_girl: Dict[str, Any] = UserGirl.update(current_session, user_girl_id, body)

  return jsonify(updateed_girl)