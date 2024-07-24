from fastapi import FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from .database import User
from .database import Movie
from .database import UserReview

from .routes import user_route
from .routes import reviews_route
from .database import database as connection
from .common import create_access_token


app = FastAPI(
    title='Proyecto en FastAPI.',
    description='Primer proyecto de aprendizaje de FastAPI y Python.',
    version='1',
)

app.include_router(user_route)
app.include_router(reviews_route)

@app.post('/users/auth')
async def auth(data: OAuth2PasswordRequestForm = Depends()):

    user = User.authenticate(data.username, data.password)

    if user:
        return {
            'access_token': create_access_token(user),
            'token_type': 'bearer',
        }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password', headers={'WWW-Authenticate': 'beraer'})

@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()

    connection.create_tables([User, Movie, UserReview])

@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()

@app.get('/')
async def index():
    return 'Hola primer servidor con FastAPI'





