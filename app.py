from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
from flask import redirect

from src.models import run_db
from src.routes.auth_routes import auth_bp
from src.routes.game_routes import game_bp
from src.routes.pokemon_routes import pokemon_bp
from datetime import timedelta

info = Info(
  title="Pokémon Idle Game API",
  version="1.0.0",
  description="API para gerenciamento de progresso, batalhas e Pokémons do Idle Game."
)

app = OpenAPI(__name__, info=info)

CORS(app, supports_credentials=True)

home_tag = Tag(name="Documentação", description="Interface de documentação")

@app.get('/', tags=[home_tag])
def home():
  """Redireciona para o Swagger UI da API."""
  return redirect('/openapi')

app.config.update(
    SECRET_KEY="Secret-key",   # Já que é um projeto educional, a key será hardcoded
    SESSION_COOKIE_SECURE=False, # Temporario para dev    
    SESSION_COOKIE_HTTPONLY=True,    
    SESSION_COOKIE_SAMESITE="Lax", # Temporario para dev
    PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
)

app.register_api(auth_bp)
app.register_api(game_bp)
app.register_api(pokemon_bp)

if __name__ == '__main__':
  run_db()
  app.run(host='0.0.0.0', port=5000, debug=True)