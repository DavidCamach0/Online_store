

# Escritorio/GIT/backend/service/user_service.py

from backend.core.database import get_cursor,get_connection
from fastapi import HTTPException, status,Depends,Request
from psycopg2 import IntegrityError
from backend.utils.hash import hash_password, verify_password
from backend.schemas.models import UserCreate, UserLogin,UserDelete,UserUpdate
from backend.utils.logger import get_logger
from backend.utils.audit import registrar_auditoria

from backend.service.token_service import generar_token, verificar_token
from backend.service.email_service import enviar_email_confirmacion
from backend.interfaces.user_interface import IUserService
from backend.interfaces.user_repository_interface import IUserRepository
logger = get_logger(__name__)





class UserService(IUserService):

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

 
    def register_user(self, request:Request,user_data: UserCreate) -> dict:


        try:
                user = self.user_repository.create_user(user_data)
                token = generar_token(user_data.email)
                enviar_email_confirmacion(user_data.email, token)

                if not user:
                    raise HTTPException(status_code=500, detail="Error al registrar usuario")

                
                        

                return user,token
            
        except IntegrityError as e:
            error_message = str(e)
           

            if "usuarios_username_key" in error_message:
                raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
            elif "usuarios_email_key" in error_message:
                raise HTTPException(status_code=400, detail="El correo ya está registrado")
            elif "usuarios_password_key" in error_message:
                raise HTTPException(status_code=400, detail="La contraseña ya fue usada (no debería ser única)")
            
            # Error por otra constraint UNIQUE
            raise HTTPException(status_code=400, detail="Datos duplicados")
    

    def email_confirm(self,request:Request,token:str):  
      
      try:  
        email = verificar_token(token)

           
        if not email:
            raise HTTPException(status_code=400, detail="Token inválido o expirado")
                    # Auditoria
                    
        user = self.user_repository.get_user_by_email(email)
                
        accion = "Usuario Registrado"
        registrar_auditoria(user["id"], accion, request)

        return {"mensaje": f"Cuenta {email} confirmada correctamente."}
      except Exception as e:
         logger.error(e)
         raise HTTPException(status_code=500, detail=str(e))

    def login_user(self, user_data: UserLogin,request: Request) -> dict:
    
  
      try:
        
        user = self.user_repository.login_user(user_data)
        
    
        if not user or not verify_password(user_data.password, user["password"]):
             raise HTTPException(status_code=401, detail="Credenciales inválidas")

            # Auditoria
            
        accion = "Inicio de sesión"
        registrar_auditoria(user["id"], accion, request)

        return {"id": user["id"], "username": user["username"]}
      
      except Exception as e:
         logger.error("Error al iniciar Sesion {}".format(e))
         raise
      
    def get_profile(self, user_data: dict) -> dict:
      
    
      try:  
        user = self.user_repository.get_me(user_data)
        if not user:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
        return user
      except Exception as e:
         logger.error("Error al ver Perfil {}".format(e))         
         raise
      
    def update_user(self,request:Request,update_user:UserUpdate,user:dict):

     try:
      

        user_db = self.user_repository.get_user_by_username(user)       
         
        if not user_db :
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if not verify_password(update_user.current_password,user_db["password"]):
            raise HTTPException(status_code=400,detail="Contraseña invalida")
        

        
        campos = update_user.model_dump(exclude_unset=True,exclude={"current_password"})

         

         

        if "new_password" in campos:
          
            campos["password"]= hash_password(campos.pop("new_password"))
        
        self.user_repository.update_user(user_db["id"],campos)
         
        
         # Auditoria
            
        accion = "Modifico Datos"
        registrar_auditoria(user_db["id"], accion, request)

        return {"message":"Usuario Actualizado"}
     except Exception as e:
        logger.error("Error al actualizar usuario{}".format(e))   
        error_message = str(e)
           

        if "usuarios_username_key" in error_message:
            raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
        elif "usuarios_email_key" in error_message:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")
        elif "usuarios_password_key" in error_message:
            raise HTTPException(status_code=400, detail="La contraseña ya fue usada (no debería ser única)")
            
            # Error por otra constraint UNIQUE
        raise HTTPException(status_code=400, detail="Datos duplicados")     
       
     

    def delete_user(self,request:Request,user_delete:UserDelete,user:dict ) -> dict:
      try:

         user_db = self.user_repository.get_user_by_username(user)         
         if not user_db :
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

         if not verify_password(user_delete.password,user_db["password"]):
            raise HTTPException(status_code=400,detail="Contraseña invalida")

         # Auditoria
           
         accion = "Se Elimino Usuario"
         registrar_auditoria(user["id"], accion, request)

         self.user_repository.delete_user(user_db["id"])


         message = {"Usuario":"Eliminado Exitosamente"}
         return message
      except Exception as e: 
         logger.error("Error al eliminar usuario{}".format(e))
         raise