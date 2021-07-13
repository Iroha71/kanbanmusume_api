from typing import Any, Dict, List
from flask import Blueprint
from flask.globals import request
from flask.json import jsonify
from flask_sqlalchemy_session import current_session
from controllers.auth import current_user_id
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.query import Query
from models.task import Task

app = Blueprint('task', __name__, url_prefix='/task')

@app.route('/', methods=['GET'])
@jwt_required()
def index():
  query: Query = current_session.query(Task)
  res: List[Task] = Task.index(query, request.args.get('category_id'))
  
  return jsonify(res)

@app.route('/<category_id>', methods=['POST'])
@jwt_required()
def create(category_id: str):
  requested_task: Dict[str, Any] = request.json.get('task')
  task: Dict[str, Any] = Task.create(current_session, requested_task, category_id, current_user_id())

  return jsonify(task)

@app.route('/<task_id>', methods=['PUT'])
@jwt_required()
def update(task_id: str):
  task: Dict[str, Any] = Task.update(current_session, request.json.get('task'), task_id)

  return jsonify(task)

@app.route('/<task_id>', methods=['DELETE'])
@jwt_required()
def delete(task_id: str):
  message: Dict[str, str] = Task.delete(current_session, task_id, current_user_id())

  return jsonify(message)
