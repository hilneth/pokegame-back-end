from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from datetime import datetime
from src.models import Base

class Caught_pokemons(Base):
  __tablename__ = 'caughtpokemons'

  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey('users.pk_users'), nullable=False)
  pokemon_id = Column(Integer, nullable=False)
  nickname = Column(String(100), nullable=True)
  level = Column(Integer, default=5, nullable=False)
  xp = Column(Integer, default=0, nullable=False)
  power = Column(Integer, default=5, nullable=False)
  shiny = Column(Boolean, default=False, nullable=False)
  caught_at = Column(DateTime, default=datetime.now(), nullable=False)

  def __init__(self, user_id:int, pokemon_id:int, level:int):
    """
    Create pokemon data

    Arguments:
      user_id: id of the owner of the pokemon
      pokemon_id: id of the obtained pokemon
      level: level of the caught pokemon
    """