from typing import Any, Dict, List, Union
from cerberus.validator import Validator
from flask import Blueprint
from flask import request
from flask.json import jsonify
from models.category import Category
from typing import Any
from flask_jwt_extended import jwt_required
from const import message, limit

app = Blueprint('category', __name__, url_prefix='/category')
v = Validator(allow_unknown=False)

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
  errors: Dict[str, str] = limit.check_validate(v, limit.CATEGORY, 'category', body)
  if len(errors) > 0:
    return jsonify(errors), 422
  created_category: Category = Category.create(body['name'])

  return jsonify(created_category.to_dict())

@app.route('/<category_id>', methods=['PUT'])
@jwt_required()
def update(category_id: str):
  body: Dict[str, str] = request.json.get('category')
  errors: Dict[str, str] = limit.check_validate(v, limit.CATEGORY, 'category', body)
  if len(errors) > 0:
    return jsonify(errors), 422
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
