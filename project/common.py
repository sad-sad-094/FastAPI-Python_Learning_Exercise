import jwt
from fastapi.security import OAuth2PasswordBearer

from datetime import datetime
from datetime import timedelta

SECRET_KEY = 'test_fastapi'

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth')

def create_access_token(user, days=7):
  
  data = {
    'user_id': user.id,
    'username': user.username,
    'expiration_date': datetime.utcnow() + timedelta(days=days),
  }

  return jwt.encode(data, SECRET_KEY, algorithm='HS256')