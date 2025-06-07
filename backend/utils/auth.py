#/Escritorio/GIT/backend/utils/auth.py
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status,Request
from datetime import timezone,timedelta,datetime
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
import os 
from dotenv import load_dotenv
from backend.core.database import   get_cursor
from typing import Optional
from uuid import uuid4

load_dotenv()

ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")

TIME_EXPIRE = 20

TIME_EXPIRE_GUEST = 15


auth = OAuth2PasswordBearer(tokenUrl="/login")

def create_token(datos:dict):

    access_token = datos.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=TIME_EXPIRE)
    
    access_token.update({"exp":expire})
    

    return  jwt.encode(access_token,SECRET_KEY,algorithm=ALGORITHM)

def create_token_guest(datos:dict):

    access_token = datos.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=TIME_EXPIRE_GUEST)
    
    access_token.update({"exp":expire})
    

    return  jwt.encode(access_token,SECRET_KEY,algorithm=ALGORITHM)


def create_guest():
    username = f"invitado_{uuid4().hex[:8]}"
    
    user = {"sub":username,"role":"invitado"}
    token = create_token_guest(user)
    return token



def verify_token(token = Depends(auth)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
     
        if role == "invitado":
            id = username
            
            return {"id":id,"sub":username,"role":role}

        # Buscar usuario en la base de datos
        with get_cursor() as cursor:
            cursor.execute("SELECT id, username, role FROM usuarios WHERE username = %s", (username,))
            user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

        
    except ExpiredSignatureError as e:
        raise credentials_exception
    except JWTError as e:
        
        raise HTTPException(status_code=400,detail=f"Acceso de Validacion Fallida: {e}")
    
    return user # Retorna id, username, role
 

def current_user(user = Depends(verify_token)):
   
   if not user or user == None:
        raise HTTPException(status_code=400, detail="Aun no ha Iniciado Sesion")
   
   return user

def require_role(roles: list[str]):
    def _require_role(user = Depends(current_user)):
        if user.get("role") not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")
        return user
    return _require_role
    