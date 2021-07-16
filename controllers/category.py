from typing import Any, Dict, List, Union
from flask import Blueprint
from flask import request
from flask.json import jsonify
from models.category import Category
from const import input_limit
from typing import Any
from flask_jwt_extended import jwt_required
from const import message

app = Blueprint('category', __name__, url_prefix='/category')

def validate_data(request_data: Dict[str, Any]) -> List[str]:
  errors: List[str] = []
  limit = { 'name': input_limit.CATEGORY_NAME }
  for data_key in limit:
    if request_data[data_key] == "" or len(request_data[data_key]) > limit[data_key]:
       errors.append(data_key)

  return errors

# --- API ---
@app.route('/', methods=['GET'])
@jwt_required()
def index():
  categories: List[str, Union[str, int]] = Category.index()
  if len(categories) <= 0:
    return jsonify(message.NOT_FOUND['message']), message.NOT_FOUND['status']
  res = [category.to_dict() for category in categories]

  return jsonify(res)

@app.route('/<category_id>', methods=['GET'])
@jwt_required()
def find(category_id: str):
  category: Category = Category.find_by_id(category_id)
  if category == None:
    return jsonify(message.NOT_FOUND['message']), message.NOT_FOUND['status']

  return jsonify(category.to_dict())

@app.route('/', methods=['POST'])
@jwt_required()
def create():
  body: Dict[str, str] = request.json.get('category')
  created_category: Category = Category.create(body['name'])

  return jsonify(created_category.to_dict())

@app.route('/<category_id>', methods=['PUT'])
@jwt_required()
def update(category_id: str):
  body: Dict[str, str] = request.json.get('category')
  category: Category = Category.update(category_id, body['name'])
  if category == None:
    return jsonify(message.NOT_FOUND['message']), message.NOT_FOUND['status']
  
  return jsonify(category.to_dict())

@app.route('/<category_id>', methods=['DELETE'])
@jwt_required()
def delete(category_id: str):
  deleted_category_name: str = Category.delete(category_id)
  if deleted_category_name == None:
    return jsonify(message.NOT_FOUND['message']), message.NOT_FOUND['status']

  return { "message": f"{ deleted_category_name }を削除しました" }
