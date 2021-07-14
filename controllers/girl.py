from typing import Any, Dict, List

from flask.json import jsonify
from models.girl import Girl
from flask import request, Blueprint
from flask_jwt_extended import jwt_required
from controllers.auth import current_user_id
from flask_sqlalchemy_session import current_session

app = Blueprint('girl', __name__, url_prefix='/girl')

@app.route('/', methods=['GET'])
def index():
  girls: List[Dict[str, Any]] = Girl.index(current_session)

  return jsonify(girls)

@app.route('/<girl_id>', methods=['GET'])
def find(girl_id: str):
  girl: Girl = Girl.find_by_id(current_session, girl_id)

  return jsonify(girl.to_dict())