from pydantic import BaseModel,EmailStr, field_validator
from typing import Optional
import re



class UserCreate(BaseModel):

    fullname:str
    username:str
    age:int
    email: EmailStr
    password: str
    role :Optional[str]  = "user"


    @field_validator('username')
    def validate_username(cls, value):
        # Solo letras, números y guion bajo, de 5 a 30 caracteres
        if not re.fullmatch(r'^[a-zA-Z0-9_]{5,30}$', value):
            raise ValueError('El nombre de usuario solo puede contener letras, números y guion bajo, y debe tener entre 3 y 30 caracteres.')
        if value.lower() in {'admin', 'root', 'superuser'}:
            raise ValueError('Este nombre de usuario está reservado.')
        return value

    @field_validator('password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres.')
        if not re.search(r'[A-Z]', value):
            raise ValueError('La contraseña debe contener al menos una letra mayúscula.')
        if not re.search(r'[a-z]', value):
            raise ValueError('La contraseña debe contener al menos una letra minúscula.')
        if not re.search(r'[0-9]', value):
            raise ValueError('La contraseña debe contener al menos un número.')
      
        if ' ' in value:
            raise ValueError('La contraseña no puede contener espacios.')
        return value
    @field_validator('age')
    def validate_edad(cls, value):
        if not (13 <= value <= 120):
            raise ValueError('La edad debe estar entre 13 y 120 años.')
        return value
    @field_validator('fullname')
    def validate_fullname(cls,value):
        if not re.search(r'^[a-zA-ZÁÉÍÓÚáéíóúñüÜ\s]{5,60}$',value):
            raise ValueError('solo se admiten letras y espacios')
        return value

class UserLogin(BaseModel):
    username: str
    password:str


class UserUpdate(BaseModel):

    fullname:Optional[str] = None
    username:Optional[str]= None
    age:Optional[int]= None
    email:Optional[str]=None
    current_password:str
    new_password:Optional[str]=None

    

    @field_validator('username')
    def validate_username(cls, value):
        # Solo letras, números y guion bajo, de 5 a 30 caracteres
        if not re.fullmatch(r'^[a-zA-Z0-9_]{5,30}$', value):
            raise ValueError('El nombre de usuario solo puede contener letras, números y guion bajo, y debe tener entre 3 y 30 caracteres.')
        if value.lower() in {'admin', 'root', 'superuser'}:
            raise ValueError('Este nombre de usuario está reservado.')
        return value

    @field_validator('new_password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres.')
        if not re.search(r'[A-Z]', value):
            raise ValueError('La contraseña debe contener al menos una letra mayúscula.')
        if not re.search(r'[a-z]', value):
            raise ValueError('La contraseña debe contener al menos una letra minúscula.')
        if not re.search(r'[0-9]', value):
            raise ValueError('La contraseña debe contener al menos un número.')
      
        if ' ' in value:
            raise ValueError('La contraseña no puede contener espacios.')
        return value
    @field_validator('age')
    def validate_edad(cls, value):
        if not (13 <= value <= 120):
            raise ValueError('La edad debe estar entre 13 y 120 años.')
        return value
    @field_validator('fullname')
    def validate_fullname(cls,value):
        if not re.search(r'^[a-zA-ZÁÉÍÓÚáéíóúñüÜ\s]{3,60}$',value):
            raise ValueError('solo se admiten letras y espacios')
        return value


class UserDelete(BaseModel):
    
    password:str