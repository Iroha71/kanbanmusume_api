from typing import Dict, List
from flask import Blueprint
from flask.globals import request
from flask.json import jsonify
from flask_jwt_extended import jwt_required
from models.task import Task
from const.message import NOT_FOUND
from const import limit
from cerberus.validator import Validator

app = Blueprint('task', __name__, url_prefix='/task')
v = Validator(allow_unknown=True)

@app.route('/', methods=['GET'])
@jwt_required()
def index():
  body = request.json.get('task')
  tasks: List[Task] = Task.index(body['category_id'])
  if len(tasks) <= 0:
    return jsonify(NOT_FOUND['message']), NOT_FOUND['status']
  res = [task.to_dict() for task in tasks]
  
  return jsonify(res)

@app.route('/<task_id>', methods=['GET'])
@jwt_required()
def find(task_id: str):
  task: Task = Task.find_by_id(task_id)
  if task == None:
    return jsonify(NOT_FOUND['message']), NOT_FOUND['status']
  
  return jsonify(task.to_dict())

@app.route('/', methods=['POST'])
@jwt_required()
def create():
  body: Dict[str, str] = request.json.get('task')
  errors: Dict[str, str] = limit.check_validate(v, limit.TASK, 'task', body)
  if len(errors):
    return jsonify(errors), 422
  created_task: Task = Task.create(body)
  if created_task == None:
    return jsonify(NOT_FOUND['message']), NOT_FOUND['status']

  return jsonify(created_task.to_dict())

@app.route('/<task_id>', methods=['PUT'])
@jwt_required()
def update(task_id: str):
  errors: Dict[str, str] = limit.check_validate(v, limit.UPDATE_TASK, 'task', request.json.get('task'))
  if len(errors) > 0:
    return jsonify(errors), 422
  task: Task = Task.update(task_id, request.json.get('task'))
  if task == None:
    return jsonify(NOT_FOUND['message']), NOT_FOUND['status']

  return jsonify(task.to_dict())

@app.route('/<task_id>', methods=['DELETE'])
@jwt_required()
def delete(task_id: str):
  message: str = Task.delete(task_id)
  if message == None:
    return jsonify(NOT_FOUND['message']), NOT_FOUND['status']

  return jsonify(message)

@app.route('/<task_id>/done', methods=['POST'])
@jwt_required()
def done_task(task_id: str):
  task: Task = Task.find_by_id(task_id)
  if task == None:
    return jsonify(NOT_FOUND['message']), NOT_FOUND['status']

  return jsonify({'message': 'done'})
