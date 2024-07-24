from fastapi import HTTPException
from fastapi import APIRouter
from fastapi.security import HTTPBasicCredentials
from fastapi import Response
from fastapi import Depends
from typing import List

from ..schemas import UserBaseModel
from ..schemas import UserRequestModel
from ..database import User
from ..schemas import ReviewResponseModel
from ..common import oauth2_schema

router = APIRouter(prefix='/users')


@router.post('', response_model=UserRequestModel)
async def create_user(user: UserBaseModel):

    if User.select().where(User.username == user.username).exists():
        raise HTTPException(409, 'El usuario ya está registrado')

    hashed_password = User.create_password(user.password)
    user = User.create(
        username=user.username,
        password=hashed_password,
    )

    return UserRequestModel(id=user.id, username=user.username)

@router.post('/login', response_model=UserRequestModel)
async def login(credentials: HTTPBasicCredentials, response: Response):
    
    user = User.select().where(User.username == credentials.username).first()

    if user is None:
        raise HTTPException(404, 'Usuario no registrado')
    
    if user.password != User.create_password(credentials.password):
        raise HTTPException(404, 'Contraseña incorrecta')
    
    response.set_cookie(key='user_id', value=user.id)
    
    return user

# @router.get('/reviews', response_model=List[ReviewResponseModel])
# async def get_reviews(user_id: int = Cookie(None)):
    
#     user = User.select().where(User.id == user_id).first()

#     if user is None:
#         raise HTTPException(404, 'Usuario no registrado')
    
#     return [user_review for user_review in user.reviews]

@router.get('/reviews')
async def get_reviews(token: str = Depends(oauth2_schema)):

    return {
        'token': token,
    }
