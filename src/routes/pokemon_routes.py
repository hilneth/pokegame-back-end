from flask import session as token_check

from flask_openapi3 import APIBlueprint, Tag

from src.models import db_session
from src.models.caught_pokemons import Caught_pokemons
from src.models.users import Users
from src.schemas.pokemon import (
  CatchPokemonSchema,
  UpdatePokemonSchema, 
  ReleasePokemonPathSchema, 
  PokemonListSchema, 
  PokemonResponseSchema
)
from src.schemas.error import ErrorSchema
from src.utils.token import validate_client

pokemon_tag = Tag(name="Pokémons", description="Gerenciamento da equipe e inventário de Pokémons")
pokemon_bp = APIBlueprint('pokemon', __name__, url_prefix='/api/v1/pokemon')


@pokemon_bp.post('/catch', tags=[pokemon_tag], responses={"201": PokemonResponseSchema, "404": ErrorSchema, "400": ErrorSchema})
@validate_client
def catch_pokemon(body: CatchPokemonSchema):
  """Regista a captura de um novo Pokémon para o treinador (POST)"""
  session = db_session()
  user_id = token_check["token"]
  trainer = session.query(Users).filter(Users.id == user_id).first()

  if not trainer:
    session.close()
    return {"message": "Treinador não encontrado"}, 404

  new_pokemon = Caught_pokemons(
    user_id=body.user_id,
    pokemon_id=body.pokemon_id,
    name=body.name,
    nickname=body.name.capitalize(), # body.nickname or 
    level=5,
    experience=0
  )

  try:
    session.add(new_pokemon)
    session.commit()
    response_data = {
      "id": new_pokemon.id,
      "pokemon_id": new_pokemon.pokemon_id,
      "name": new_pokemon.name,
      "nickname": new_pokemon.nickname,
      "level": new_pokemon.level,
      "experience": new_pokemon.experience
    }
    return response_data, 201
  except Exception as e:
    session.rollback()
    return {"message": "Erro ao registrar a captura do Pokémon"}, 400
  finally:
    session.close()


@pokemon_bp.get('/trainer/', tags=[pokemon_tag], responses={"200": PokemonListSchema, "404": ErrorSchema})
@validate_client
def list_trainer_pokemons():
  """Lista todos os Pokémons capturados de um determinado treinador (GET)"""
  user_id = token_check["token"]
  session = db_session()
  
  pokemons = session.query(Caught_pokemons).filter(Caught_pokemons.user_id == user_id).all() # type: ignore

  result = [
    {
      "id": p.id,
      "pokemon_id": p.pokemon_id,
      "name": p.name,
      "nickname": p.nickname,
      "level": p.level,
      "experience": p.experience,
      "sprite": p.sprite
    }
    for p in pokemons
  ]

  session.close()
  return {"pokemons": result}, 200


@pokemon_bp.put('/update', tags=[pokemon_tag], responses={"200": PokemonResponseSchema, "404": ErrorSchema, "400": ErrorSchema})
@validate_client
def update_pokemon_level(body: UpdatePokemonSchema):
  """Atualiza o nível e XP de um Pokémon específico (PUT)"""
  session = db_session()
  pokemon = session.query(Caught_pokemons).filter(Caught_pokemons.id == body.pokemon_instance_id).first()

  if not pokemon:
    session.close()
    return {"message": "Pokémon não encontrado no banco de dados"}, 404

  pokemon.level = body.level
  pokemon.experience = body.experience

  try:
    session.commit()
    response_data = {
      "id": pokemon.id,
      "pokemon_id": pokemon.pokemon_id,
      "name": pokemon.name,
      "nickname": pokemon.nickname,
      "level": pokemon.level,
      "experience": pokemon.experience
    }
    return response_data, 200
  except Exception as e:
    session.rollback()
    return {"message": "Erro ao atualizar o Pokémon"}, 400
  finally:
    session.close()


@pokemon_bp.delete('/<int:pokemon_id>', tags=[pokemon_tag], responses={"200": None, "404": ErrorSchema})
@validate_client
def release_pokemon(path: ReleasePokemonPathSchema):
  """Libera/Solta um Pokémon capturado (DELETE)"""
  session = db_session()
  pokemon = session.query(Caught_pokemons).filter(Caught_pokemons.id == path.pokemon_id).first()

  if not pokemon:
    session.close()
    return {"message": "Pokémon não encontrado no seu inventário"}, 404

  try:
    session.delete(pokemon)
    session.commit()
    return {"message": f"Pokémon '{pokemon.nickname}' foi liberado com sucesso!"}, 200
  except Exception as e:
    session.rollback()
    return {"message": "Erro ao soltar o Pokémon"}, 500
  finally:
    session.close()