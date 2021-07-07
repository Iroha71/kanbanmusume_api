from flask import Flask
from flask_jwt import JWT
from controllers.auth import authenticate, identity
from controllers import auth

"""BluePrintでコントローラーとURLのマッピングを行う
参考：https://qiita.com/keichiro24/items/c72c57b54332431c67ec
"""
app = Flask(__name__)
app.register_blueprint(auth.app, url_prefix="/api")
app.config['SECRET_KEY'] = 'super-secret'
jwt = JWT(app, authenticate, identity)

if __name__ == "__main__":
  app.run(debug=True, port=5500)