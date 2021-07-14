from typing import Any, Dict, List
from flask import Blueprint
from flask.globals import request
from flask.json import jsonify
from flask_sqlalchemy_session import current_session
from controllers.auth import current_user_id
from flask_jwt_extended import jwt_required
from models.task import Task
from const import message

app = Blueprint('task', __name__, url_prefix='/task')

@app.route('/', methods=['GET'])
@jwt_required()
def index():
  tasks: List[Task] = Task.index(current_session, request.args.get('category_id'))
  if len(tasks) <= 0:
    msg: Dict[str, Any] = message.set_notfound('タスク')
    return jsonify(msg['message']), msg['status']
  
  return jsonify(tasks)

@app.route('/<task_id>', methods=['GET'])
@jwt_required()
def find(task_id: str):
  task: Task = Task.find_by_id(current_session, task_id)
  if task == None:
    notfound: Dict[str, int] = message.set_notfound('タスク')
    return jsonify(notfound['message']), notfound['status']
  
  return jsonify(task.to_dict())

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
