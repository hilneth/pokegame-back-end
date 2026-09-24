from pydantic import BaseModel, Field

class ErrorSchema(BaseModel):
  """Schema para mensagens de erro padronizadas na API"""
  message: str