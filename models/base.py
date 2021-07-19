from typing import Any, Dict, List, Union
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.query import Query
from flask_sqlalchemy_session import current_session

Base = declarative_base()

def get_query(cls_obj: Any, query: Query) -> Query:
  if query==None:
    return current_session.query(cls_obj)
  else:
    return query