import requests

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon/"

def fetch_pokemon_from_pokeapi(pokemon_id: int):
  """
  Consome a PokéAPI pública e retorna os dados resumidos do Pokémon (Gen 1 ou 2).
  """
  try:
    response = requests.get(f"{POKEAPI_URL}{pokemon_id}", timeout=5)
    if response.status_code == 200:
      data = response.json()
      return {
        "pokemon_id": data["id"],
        "name": data["name"],
        "base_experience": data["base_experience"],
        "sprite_front": data["sprites"]["front_default"],
        "types": [t["type"]["name"] for t in data["types"]]
      }
    return None
  except Exception:
    return None

def fetch_sprite_from_pokeapi(pokemon_id: int):
  """
  Consome a PokéAPI pública e retorna o sprite
  """
  try:
    response = requests.get(f"{POKEAPI_URL}{pokemon_id}", timeout=5)
    if response.status_code == 200:
      data = response.json()
      return data["sprites"]["front_default"]
    return None
  except Exception:
    return None