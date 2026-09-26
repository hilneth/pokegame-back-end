from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from datetime import datetime
from src.services.pokeapi_service import fetch_pokemon_from_pokeapi, fetch_sprite_from_pokeapi
from src.models import Base

class Caught_pokemons(Base):
  __tablename__ = 'caughtpokemons'

  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey('users.pk_users'), nullable=False)
  pokemon_id = Column(Integer, nullable=False)
  name = Column(String(100), nullable=False)
  nickname = Column(String(100), nullable=True)
  level = Column(Integer, default=5, nullable=False)
  experience = Column(Integer, default=0, nullable=False)
  sprite = Column(String(500), nullable=False)
  caught_at = Column(DateTime, default=datetime.now(), nullable=False)

  def __init__(self, user_id:int, pokemon_id:int, level:int, experience: int, name:str, nickname:str):
    """
    Create pokemon data

    Arguments:
      user_id: id of the owner of the pokemon
      pokemon_id: id of the obtained pokemon
      level: level of the caught pokemon
      experience: current experience of the pokemon
      name: name of the pokemon
      nickname: nickname of the pokemon
    """

    self.user_id = user_id
    self.pokemon_id = pokemon_id
    self.level = level
    self.experience = experience
    self.name = name
    self.nickname = nickname
    self.sprite = fetch_sprite_from_pokeapi(pokemon_id) # type: ignore