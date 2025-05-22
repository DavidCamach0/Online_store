from fastapi import APIRouter, HTTPException, Depends,status,Request
from fastapi.security import OAuth2PasswordRequestForm
from backend.schemas.models import UserCreate, UserDelete, UserUpdate
from backend.utils.utils import hash_password, verify_password
from backend.utils.auth import create_token, verify_token
from backend.service.user_service import UserService
from backend.utils.logger import get_logger



router = APIRouter( prefix="/user",
    tags=["user"]   )

user_service = UserService()

logger = get_logger(__name__)

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


@router.post("/Register")
async def Register(request:Request,user: UserCreate):
    try:
        new_user = user_service.register_user(request,user)
        
        return {"message": "Usuario registrado correctamente", "user": new_user}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Error al Registar Usuario {}".format(e))        
        raise  HTTPException(status_code=500, detail="Error interno del servidor")
    

@router.post("/login")   
async def login(request:Request,user: OAuth2PasswordRequestForm = Depends() ):
   
   try:

        user_db = user_service.login_user(user,request)
        
        token = create_token({"sub":user_db["username"],"role":user_db["role"]})
        
        return {"message":"Inision de sesion Exitosa",
                "username":user_db["username"],
                "role":user_db["role"],"token":token} 
   except HTTPException as e:
        raise e
   except Exception as e:     
        logger.error("Error al iniciar Sesion {}".format(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    

@router.get("/me")
async def me(user: dict = Depends(current_user)):
   try:
        profile = user_service.get_profile(user)
        return {"Mi Perfil":profile}
   except HTTPException as e:
        raise e
   except Exception as e:     
        logger.error("Error al Mostrar Perfil {}".format(e))      
        raise HTTPException(status_code=500, detail="Error interno del servidor")   


@router.put("/mi-perfil")
async def update(request:Request,update:UserUpdate,user:dict = Depends(current_user)):

   try:   
        message=user_service.update_user(request,update,user)
        return message
   except HTTPException as e:
        raise e
   except Exception as e:
        logger.error("Error al Actualizar Usuario {}".format(e))       
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
     
@router.delete("/delete-account")
async def deleteUser(request:Request,user_delete:UserDelete,user:dict = Depends(current_user)):

   try:
        message = user_service.delete_user(request,user_delete,user)

        return message
   except HTTPException as e:
        raise e
   except Exception as e:
        logger.error("Error al Eliminar Usuario {}".format(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")



  