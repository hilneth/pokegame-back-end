import random
from flask_openapi3 import APIBlueprint, Tag
from sqlalchemy import func

from src.models import db_session
from src.models.users import Users
from src.models.caught_pokemons import Caught_pokemons
from src.schemas.trainer import (
  UserUpdateProgressSchema, 
  UserResponseSchema, 
  LeaderboardListSchema
)
from src.schemas.pokemon import GetPokemonFromAPI
from src.schemas.error import ErrorSchema
from src.services.pokeapi_service import fetch_pokemon_from_pokeapi

game_tag = Tag(name="Jogo e Progresso", description="Rotas de mecânica de jogo, encontros e classificações")
game_bp = APIBlueprint('game', __name__, url_prefix='/api/v1/game')

@game_bp.get('/leaderboard', tags=[game_tag], responses={"200": LeaderboardListSchema})
def leaderboard():
  """Retorna a classificação dos treinadores ordenados por moedas acumuladas (GET)"""
  session = db_session()
  user_list = session.query(Users).order_by(Users.currency.desc()).limit(10).all() # type: ignore

  result = []
  for t in user_list:
    total_pokemons = session.query(func.count(Caught_pokemons.id)).filter(Caught_pokemons.user_id == t.id).scalar() # type: ignore
    result.append({
      "username": t.username,
      "coins": t.currency,
      "total_pokemons": total_pokemons or 0
    })

  session.close()
  return {"leaderboard": result}, 200


@game_bp.get('/encounter', tags=[game_tag], responses={"200": GetPokemonFromAPI, "502": ErrorSchema}) # type: ignore
def wild_encounter():
  """Sorteia um Pokémon selvagem entre a Gen 1 e Gen 2 (IDs 1 a 251) consumindo a PokéAPI (GET)"""
  random_id = random.randint(1, 251)
  pokemon_data = fetch_pokemon_from_pokeapi(random_id)

  if not pokemon_data:
    return {"message": "Falha ao obter dados da PokéAPI pública"}, 502

  return pokemon_data, 200


@game_bp.put('/progress', tags=[game_tag], responses={"200": UserResponseSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_progress(body: UserUpdateProgressSchema):
  """Atualiza o progresso do Treinador (Moedas e Rota atual) (PUT)"""
  session = db_session()
  user = session.query(Users).filter(Users.id == body.user_id).first()

  if not user:
    session.close()
    return {"message": "Treinador não encontrado"}, 404

  if body.currency is not None:
    user.currency = body.currency
  if body.last_route is not None:
    user.last_route = body.last_route # type: ignore

  try:
    session.commit()
    response_data = {
      "id": user.id,
      "username": user.username,
      "currency": user.currency,
      "last_route": user.last_route
    }
    return response_data, 200
  except Exception as e:
    session.rollback()
    return {"message": "Erro ao salvar progresso do treinador"}, 400
  finally:
    session.close()