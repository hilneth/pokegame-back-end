# Pokémon Idle Game - API Back-End

API REST desenvolvida em Python com Flask para suporte a mecânicas de um Idle Game baseado na 1ª e 2ª Geração de Pokémon. Projeto desenvolvido para a Pósgraduação de desenvolvimento de software da PUC-RJ.
Projeto tem que ser utilizado em conjunto com o front-end, que pode ser encontrado aqui:
https://github.com/hilneth/pokegame-front-end 

## Funcionalidades
- Autenticação e cadastro de treinadores (com suporte a hash de senha).
- Consulta de Pokémon selvagem via **PokéAPI pública** (IDs 1 a 251).
- Atualização de progresso do jogador (moedas, rota e Pokémons).
- Tabela de Classificação (Leaderboard).
- Documentação interativa via **Swagger UI** (`flask-openapi3`).

## Tecnologias Utilizadas
- **Python 3.10** + **Flask**
- **Flask-OpenAPI3** & **Pydantic**
- **SQLAlchemy** + **SQLite**
- **Docker**

## Documentação e Rotas da API (Swagger)
Com o container em execução, acesse no navegador:
`http://localhost:5000/openapi`

### Métodos HTTP Implementados
- `POST`: `/api/v1/auth/register`, `/api/v1/auth/login`, `/api/v1/pokemon/catch`
- `GET`: `/api/v1/game/leaderboard`, `/api/v1/game/encounter`, `/api/v1/pokemon/trainer/`
- `PUT`: `/api/v1/game/progress`, `/api/v1/pokemon/update`
- `DELETE`: `/api/v1/pokemon/<id>`

## API Externa Consumida
- **Nome**: PokéAPI
- **URL**: `https://pokeapi.co/api/v2/pokemon/{id}`
- **Descrição**: Usada para buscar dados, sprites e experiência base de Pokémons entre as Gerações 1 e 2. 

## Execução via Docker
```bash
# Gerar a imagem do container
docker build -t pokeidle-back .

# Executar o container na porta 3000
docker run -d -p 5000:5000 --name pokeidle-back pokeidle-back