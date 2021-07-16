from typing import List
from flask.json import jsonify
from models.girl import Girl
from flask import Blueprint

app = Blueprint('girl', __name__, url_prefix='/girl')

@app.route('/', methods=['GET'])
def index():
  girls: List[Girl] = Girl.index()
  res = [girl.to_dict() for girl in girls]

  return jsonify(res)

@app.route('/<girl_id>', methods=['GET'])
def find(girl_id: str):
  girl: Girl = Girl.find_by_id(girl_id)

  return jsonify(girl.to_dict())