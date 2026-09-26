from pydantic import BaseModel, Field
from typing import Optional, List

class CatchPokemonSchema(BaseModel):
  """Schema para registrar a captura de um novo Pokémon (POST)"""
  user_id: int = Field(description="ID do Treinador que capturou", default=1)
  pokemon_id: int = Field(description="ID do Pokémon na PokéAPI (1 a 251)", default=25)
  name: str = Field(description="Nome da espécie do Pokémon", default="pikachu")
  nickname: Optional[str] = Field(description="Apelido opcional dado ao Pokémon", default="Pika")


class UpdatePokemonSchema(BaseModel):
  """Schema para atualizar o nível e XP de um Pokémon (PUT/PATCH)"""
  pokemon_instance_id: int = Field(description="ID da instância do Pokémon no banco de dados", default=10)
  level: int = Field(description="Novo nível atingido pelo Pokémon", default=15)
  experience: int = Field(description="Nova quantidade de experiência acumulada", default=1200)


class ReleasePokemonPathSchema(BaseModel):
  """Schema para pegar o ID na URL ao soltar/deletar um Pokémon (DELETE)"""
  pokemon_id: int = Field(description="ID da instância do Pokémon a ser removido/liberado", default=10)


class PokemonResponseSchema(BaseModel):
  """Schema com os detalhes de um Pokémon capturado"""
  id: int = Field(description="ID da instância no banco local", default=10)
  pokemon_id: int = Field(description="ID original na PokéAPI", default=25)
  name: str = Field(description="Nome da espécie do Pokémon", default="pikachu")
  nickname: Optional[str] = Field(description="Apelido do Pokémon", default="Pika")
  level: int = Field(description="Nível do Pokémon", default=5)
  sprite: str
  experience: int = Field(description="XP acumulado", default=100)


class PokemonListSchema(BaseModel):
  """Schema para listagem de Pokémons do time/inventário do jogador (GET)"""
  pokemons: List[PokemonResponseSchema]

class GetPokemonFromAPI(BaseModel):
  """Schema de resposta com informações do pokemon"""
  
  pokemon_id: int
  name: str
  base_experience: int
  sprite_front: str
  types: str