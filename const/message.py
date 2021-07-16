from typing import Dict


NOT_HAVE_ROLE_EDIT = { "message": { "error": "編集権限がありません" }, "status": 403 }
NOT_HAVE_ROLE_WATCH = { "message": { "error": "閲覧権限がありません" }, "status": 403 }
DUPLICATE_RECORD = { "message": { "error": "値が重複しています" }, "status": 200 }
LOGIN_FAILD = { "message": { "error": "ユーザ名またはパスワードが違います" }, "status": 401 }
NOT_FOUND = { "message": { "error": "対象が見つかりませんでした" }, "status": 404 }

def set_notfound(content: str) -> Dict[str, int]:
  """コンテンツが見つからない場合のエラーメッセージを作る

  Args:
      content (str): メッセージに入れたいコンテンツ名

  Returns:
      str: not found メッセージ
  """
  return { "message": { f"{ content }は見つかりませんでした" }, "status": 404 }