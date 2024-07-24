from pydantic import field_validator
from pydantic import BaseModel
from pydantic.utils import GetterDict
from typing import Any
from peewee import ModelSelect

class PeeweeGetterDict(GetterDict):
  def get(self, key: Any, default: Any = None):
    
    resp= getattr(self._obj, key, default)

    if isinstance(resp, ModelSelect):
      return list(resp)
    
    return resp

class UserBaseModel(BaseModel):
  username:str
  password:str

  @field_validator('username')
  def username_validator(cls, username):
    if len(username) < 3 or len(username) > 50:
      raise ValueError('La longitud debe ser dentro de un rango de 3 y 50 caracteres.')
    return username
  
class UserRequestModel(BaseModel):
  id: int
  username: str

class ResponseModel(BaseModel):
    class Config:
        orm_mode = True,
        getter_dict = PeeweeGetterDict,

class ReviewValidator():
    @field_validator('score')
    def score_validator(cls, score):
        if score < 1 or score > 5:
          raise ValueError('El rango para el score es entre 1 y 5')
        
        return score

class MovieResponseModel(ResponseModel):
   id: int
   title: str

class ReviewRequestModel(ResponseModel, ReviewValidator):
    user_id: int
    movie_id: int
    review: str
    score: int       

class ReviewResponseModel(ResponseModel):
    id: int
    movie: MovieResponseModel
    review: str
    score: int

class ReviewRequestPutModel(BaseModel, ReviewValidator):
    review: str
    score: int

