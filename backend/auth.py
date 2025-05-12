from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException
from datetime import timezone,timedelta,datetime
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
import os 
from dotenv import load_dotenv

load_dotenv()

ALGORITHMO = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")

TIME_EXPIRE = 15




auth = OAuth2PasswordBearer(tokenUrl="/login")

def create_token(datos:dict):

    access_token = datos.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=TIME_EXPIRE)
    
    access_token.update({"exp":expire})
    

    return  jwt.encode(access_token,SECRET_KEY,algorithm=ALGORITHMO)


def verify_token(token = Depends(auth)):
    try:
        user = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHMO).get("sub")
    except ExpiredSignatureError as e:
        raise HTTPException(status_code=400,detail=f"Tiempo de Sesion Expirada:  {e}")
    except JWTError as e:
        
        raise HTTPException(status_code=400,detail=f"Acceso de Validacion Fallida: {e}")

    return user
 

    