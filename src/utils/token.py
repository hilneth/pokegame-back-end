from functools import wraps
from flask import session as token_check, request


def validate_client(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    token = token_check.get("token")
    if not token:
      error_msg = "Unauthorized"
      return {"message": error_msg}, 403
    
    response = f(*args, **kwargs)

    return response
  return decorated_function