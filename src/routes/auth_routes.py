from flask_openapi3 import APIBlueprint, Tag
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from src.models import db_session
from src.models.users import Users
from src.schemas.trainer import TrainerRegisterSchema, TrainerLoginSchema, TrainerResponseSchema
from src.schemas.error import ErrorSchema

auth_tag = Tag(name="Autenticação", description="Criação de conta e Login do Treinador")
auth_bp = APIBlueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.post('/register', tags=[auth_tag], responses={"201": TrainerResponseSchema, "400": ErrorSchema, "409": ErrorSchema})
def register(body: TrainerRegisterSchema):
  """Cadastra um novo Treinador de Pokémon"""
  session = db_session()
  
  if session.query(Users).filter(Users.username == body.username).first(): # type: ignore
    session.close()
    return {"message": "Nome de treinador ou Email já está em uso"}, 409

  if session.query(Users).filter(Users.email == body.email).first(): # type: ignore
    session.close()
    return {"message": "Nome de treinador ou Email já está em uso"}, 409

  new_trainer = Users(
    username=body.username,
    email=body.email,
    password=generate_password_hash(body.password),
    currency=100
  )

  try:
    session.add(new_trainer)
    session.commit()
    response_data = {
      "username": new_trainer.username,
      "coins": new_trainer.currency,
    }
    return response_data, 201
  except Exception as e:
    session.rollback()
    print(e)
    return {"message": "Erro ao criar conta de treinador"}, 400
  finally:
    session.close()