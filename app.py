from flask import Flask
from flask_sqlalchemy_session import flask_scoped_session
from database import session as dbsession
from database import SQLALCHEMY_DATABASE_URI
from flask_jwt_extended import JWTManager
from controllers import auth, user, category, task, girl, user_girl

"""BluePrintで各コントローラに処理を振り分ける
"""
app = Flask(__name__)
session = flask_scoped_session(dbsession, app)
app.register_blueprint(auth.app)
app.register_blueprint(user.app)
app.register_blueprint(category.app)
app.register_blueprint(task.app)
app.register_blueprint(girl.app)
app.register_blueprint(user_girl.app)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# JSONのソートを抑止
app.config['JSON_SORT_KEYS'] = False
app.config['JWT_SECRET_KEY'] = 'secret-key'   # JWTに署名する際の秘密鍵
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)

if __name__ == '__main__':
  app.run(debug=True, port=5500)