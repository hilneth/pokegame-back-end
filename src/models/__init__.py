from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

from src.models.base import Base
from src.models.users import Users
from src.models.caught_pokemons import Caught_pokemons

db_path = "database/"
if not os.path.exists(db_path):
  os.makedirs(db_path)

db_url = 'sqlite:///%s/db.sqlite3' % db_path

engine = create_engine(db_url, echo=False)

db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def run_db():
  if not database_exists(engine.url):
    create_database(engine.url) 
  Base.metadata.create_all(engine)