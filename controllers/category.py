from typing import Any, Dict, List
from flask import Blueprint
from flask import request
from flask.json import jsonify
from models.category import Category
from flask_sqlalchemy_session import current_session
from sqlalchemy.orm.query import Query
from const import input_limit
from typing import Any
from flask_jwt_extended import jwt_required, get_jwt_identity
from const import message

app = Blueprint('category', __name__, url_prefix='/category')

def find_category(category_id: int) -> Category:
  """指定IDのカテゴリを取得する

  Args:
      category_id (int): 検索対象のカテゴリID

  Returns:
      Category: 該当IDのカテゴリ情報
  """
  query: Query = current_session.query(Category)
  category: Category = query.filter(Category.id==category_id).first()

  return category

def get_current_user_id():
  return get_jwt_identity()

def can_edit(target_category: Category) -> bool:
  """データ編集が可能なユーザか検証する

  Args:
      target_category (Category): 編集対象のカテゴリオブジェクト

  Returns:
      bool: 編集可能なユーザか
  """

  return get_current_user_id() == target_category.user_id

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
  query: Query = current_session.query(Category)
  categories: List[Category] = query.filter(Category.user_id==get_current_user_id()).all()
  categories_json = []
  for category in categories:
    categories_json.append(category.to_dict())

  return jsonify(categories_json)

@app.route('/<category_id>', methods=['GET'])
@jwt_required()
def find(category_id: str):
  category: Category = find_category(category_id)
  if not can_edit(category):
    return message.NOT_HAVE_ROLE_WATCH
  return category.to_dict()

@app.route('/', methods=['POST'])
@jwt_required()
def create():
  requested_category: Dict[str, Any] = request.json
  check_errors = validate_data(requested_category)
  if len(check_errors) > 0:
    return jsonify({"errors": check_errors})
  category: Category = Category(name=requested_category['name'], user_id=get_current_user_id())
  current_session.add(category)
  current_session.commit()

  return jsonify(category.to_dict())

@app.route('/<category_id>', methods=['POST'])
@jwt_required()
def update(category_id: str):
  category: Category = find_category(category_id)
  if not can_edit(category):
    return message.NOT_HAVE_ROLE_EDIT
  
  category = category.update(request.json.get('name', None))
  current_session.commit()
  return jsonify(category.to_dict())

@app.route('/<category_id>', methods=['DELETE'])
@jwt_required()
def delete(category_id: str):
  category: Category = find_category(category_id)
  category_name = category.name
  if not can_edit(category):
    return message.NOT_HAVE_ROLE_EDIT
  current_session.delete(category)
  current_session.commit()

  return { "message": f"{ category_name }を削除しました" }
