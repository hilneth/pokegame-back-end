from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from typing import Union

from src.models import Base


class Users(Base):
  __tablename__ = 'users'

  id = Column('pk_users', Integer, primary_key=True)
  hash_password = Column(String(255), nullable=False)
  email = Column(String(100), unique=True, nullable=False)
  username = Column(String(100), nullable=False)
  progress = Column(Integer, default=0)
  currency = Column(Integer, default=0)
  last_route = Column(String(100), default="Pallet Town")
  last_login = Column(DateTime, default=datetime.now)
  created_at = Column(DateTime, default=datetime.now)

  def __init__(self, username:str, email:str, password:str, currency:int):
    """
    Create a new User

    Arguments:
    email: user email
    hash_password: user hashed password
    username: user selected name
    creation_time: time that the data was added
    """

    self.email = email.lower()
    self.hash_password = password
    self.username = username 
    self.currency = currency