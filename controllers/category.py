from typing import Any, Dict, List
from flask import Blueprint
from flask import request
from flask import json
from flask.json import jsonify
from models.category import Category
from flask_sqlalchemy_session import current_session
from sqlalchemy.orm.query import Query
from models.category import Category
from const import input_limit

app = Blueprint('category', __name__, url_prefix='/category')

def validate_data(request_data: Dict[str, Any]) -> List[str]:
  errors: List[str] = []
  limit = { 'name': input_limit.CATEGORY_NAME }
  for data_key in limit:
    if request_data[data_key] == "" or len(request_data[data_key]) > limit[data_key]:
       errors.append(data_key)

  return errors

@app.route('/', methods=['GET'])
def index():
  user_id: str = request.args.to_dict()['user_id']
  query: Query = current_session.query(Category)
  categories: List[Category] = query.filter(Category.user_id==user_id).all()
  categories_json = []
  for category in categories:
    categories_json.append(category.to_dict())

  return jsonify(categories_json)

@app.route('/', methods=['POST'])
def create():
  requested_category: Dict[str, Any] = request.json
  check_errors = validate_data(requested_category)
  if len(check_errors) > 0:
    return jsonify({"errors": check_errors})
  category: Category = Category(name=requested_category['name'], user_id=requested_category['user_id'])
  category.create(current_session)

  return jsonify(category.to_dict())

# @app.route('/<category_id>', methods=['POST'])
# def update(category_id: str):
#   Category.update(current_session, )