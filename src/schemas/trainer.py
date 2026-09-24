from email.policy import default
from locale import currency

from pydantic import BaseModel, Field
from typing import Optional, List

class TrainerRegisterSchema(BaseModel):
    """Schema para cadastro de um novo Treinador (POST)"""
    username: str = Field(description="Nome de usuário do treinador", default="AshKetchum")
    email: str = Field(description="Email do usuário", default="ash.ketchum@email.com")
    password: str = Field( description="Senha do treinador", default="pikachu123")


class TrainerLoginSchema(BaseModel):
    """Schema para login do Treinador (POST)"""
    username: str = Field(description="Nome de usuário", default="AshKetchum")
    password: str = Field(description="Senha", default="pikachu123")


class TrainerUpdateProgressSchema(BaseModel):
    """Schema para atualizar o progresso do jogo/treinador (PUT/PATCH)"""
    trainer_id: int = Field(description="ID do Treinador", default=1)
    currency: Optional[int] = Field(description="Nova quantidade total de moedas", default=250)
    last_route: Optional[str] = Field(description="Rota atual em que o jogador se encontra (1 a 26)", default="2")


class TrainerResponseSchema(BaseModel):
    """Schema de resposta com dados do Treinador"""
    id: int = Field(description="ID do Treinador", default=1)
    username: str = Field(description="Nome do Treinador", default="AshKetchum")
    currency: int = Field(description="Quantidade atual de moedas", default=150)
    last_route: str = Field(description="Rota atual do jogador", default="1")


class LeaderboardItemSchema(BaseModel):
    """Schema para exibir a classificação dos jogadores no Leaderboard (GET)"""
    username: str = Field(description="Nome do Treinador", default="AshKetchum")
    currency: int = Field(description="Moedas acumuladas", default=1500)
    total_pokemons: int = Field(description="Total de Pokémons capturados", default=12)


class LeaderboardListSchema(BaseModel):
    """Schema para lista de classificação (GET /leaderboard)"""
    leaderboard: List[LeaderboardItemSchema]