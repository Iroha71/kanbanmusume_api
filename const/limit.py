from typing import Any, Dict, List
from cerberus.validator import Validator

# """入力制限を定義
# """
USER = {
  'name': {'required': True, 'maxlength': 30, 'empty': False },
  'nickname': {'required': True, 'empty': False, 'maxlength': 10 },
  'password': { 'required': True, 'minlength': 6, 'maxlength': 30 }
}
UPDATE_USER = {
  'nickname': USER['nickname']
}

CATEGORY = {
  'name': {'required': True, 'maxlength': 20, 'empty': False}
}

error_messages = {
  'user': {
    'name': 'ユーザ名は' + str(USER['name']['maxlength']) + '文字以下で入力してください',
    'nickname': '呼び名は' + str(USER['nickname']['maxlength']) + '文字以下で入力してください',
    'password': f"パスワードは{USER['password']['minlength']}~{USER['password']['maxlength']}文字の英数字・記号で入力してください"
  },
  'category': {'name': f"カテゴリ名は{CATEGORY['name']['maxlength']}文字以下で入力してください" }
}

def check_validate(v: Validator, rule: Dict[str, Any], schemaname: str, req: Dict[str, str]) -> Dict[str, str]:
  """バリデーションを行う

  Args:
      v (Validator): バリデーションオブジェクト
      rule (Dict[str, Any]): バリデーションルールオブジェクト
      schemaname (str): エラーメッセージを記載しているスキーマ名
      req (Dict[str, str]): リクエストの内容

  Returns:
      Dict[str, str]: エラーメッセージの辞書
  """
  v.validate(req, rule)
  errors: Dict[str, List[str]] = v.errors
  if len(errors) <= 0:
    return errors
  error_msgs = {}
  for key, value in errors.items():
    error_msgs[key] = error_messages[schemaname][key]
  
  return error_msgs
