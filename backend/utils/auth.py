from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from datetime import timezone,timedelta,datetime
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
import os 
from dotenv import load_dotenv
from backend.db.db import   get_cursor
load_dotenv()

ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")

TIME_EXPIRE = 15




auth = OAuth2PasswordBearer(tokenUrl="/login")

def create_token(datos:dict):

    access_token = datos.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=TIME_EXPIRE)
    
    access_token.update({"exp":expire})
    

    return  jwt.encode(access_token,SECRET_KEY,algorithm=ALGORITHM)


def verify_token(token = Depends(auth)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

        # Buscar usuario y su rol en la base de datos
        with get_cursor() as cursor:
            cursor.execute("SELECT id, username, role FROM usuarios WHERE username = %s", (username,))
            user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

        
    except ExpiredSignatureError as e:
        raise HTTPException(status_code=400,detail=f"Tiempo de Sesion Expirada:  {e}")
    except JWTError as e:
        
        raise HTTPException(status_code=400,detail=f"Acceso de Validacion Fallida: {e}")
    
    return user # Retorna id, username, role
 

    