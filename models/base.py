from typing import Any, Dict, List
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def convert_object2dict(objects: List[Any]) -> Dict[str, Any]:
  """オブジェクト配列を辞書型配列に変換する

  Args:
      objects (List[Any]): オブジェクト配列

  Returns:
      Dict[str, Any]: 辞書配列
  """
  result = []
  for obj in objects:
    result.append(obj.to_dict())
  
  return result