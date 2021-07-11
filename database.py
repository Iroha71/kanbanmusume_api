from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/kanbanmusume'
# engine = create_engine('sqlite:///test.db')
engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = sessionmaker(bind=engine)