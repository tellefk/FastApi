from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:asdqwe123@localhost/TodoAppDatabase"

"""
for sqlite
# """
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

"""
for postgresql
"""
engine=create_engine(SQLALCHEMY_DATABASE_URL)


"""
create a instance of the session of the database 
"""
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()