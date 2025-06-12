#/Escritorio/GIT/backend/routers/users.py

from fastapi import APIRouter, HTTPException, Depends,status,Request,Query
from fastapi.security import OAuth2PasswordRequestForm
from backend.schemas.user_schema import UserCreate, UserDelete, UserUpdate
from backend.utils.auth import create_token,current_user,create_guest
from backend.service.user_service import UserService
from backend.utils.logger import get_logger
from backend.repositories.user_repository_postgres import UserRepositoryPostgres
from backend.service.user_service import UserService


router = APIRouter( prefix="/user",
    tags=["user"]   )


logger = get_logger(__name__)

user_repo = UserRepositoryPostgres()
user_service = UserService(user_repo)



@router.post("/Register")
async def Register(request:Request,user: UserCreate):
    try:
        new_user = user_service.register_user(request,user)
        
        return {"message": "Usuario registrado correctamente", "user": new_user[0],"token":new_user[1]}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Error al Registar Usuario {}".format(e))        
        raise  HTTPException(status_code=500, detail="Error interno del servidor")
    
@router.get("/confirmar-email")
def confirmar_email(request:Request,token: str = Query(...)):
     
     try:
          user_service.email_confirm(request,token)
          return {"correo":"confirmado"} 
     except Exception as e:
         logger.error(e)
         raise HTTPException(status_code=500, detail=e)

@router.post("/login")   
async def login(request:Request,user: OAuth2PasswordRequestForm = Depends() ):
   
   try:

        user_db = user_service.login_user(user,request)
        
        token = create_token({"sub":user_db["username"]})
        
        return {"message":"Inision de sesion Exitosa",
                "username":user_db["username"],"token":token} 
   
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



  