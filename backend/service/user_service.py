

# services/user_service.py

from backend.db.db import get_cursor,get_connection
from fastapi import HTTPException, status,Depends,Request
from psycopg2 import IntegrityError
from backend.utils.utils import hash_password, verify_password
from backend.schemas.models import UserCreate, UserLogin,UserDelete,UserUpdate
from backend.utils.logger import get_logger
from backend.utils.audit import registrar_auditoria
from psycopg2.extras import RealDictCursor

logger = get_logger(__name__)





class UserService:
    def register_user(self, request:Request,user_data: UserCreate) -> dict:
        try:
            with get_connection() as conn:
                cursor=conn.cursor(cursor_factory=RealDictCursor)
                

                hashed_pwd = hash_password(user_data.password)
                cursor.execute(
                    """
                    INSERT INTO usuarios (fullname, username, email, age, password, role)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id, username, email
                    """,
                    (
                        user_data.fullname,
                        user_data.username,
                        user_data.email,
                        user_data.age,
                        hashed_pwd,
                        user_data.role
                    )
                )

                
                user = cursor.fetchone()
                
                if user:
                    cursor.close()
                    conn.commit()
                        
                    # Auditoria
                    

                
                    accion = "Usuario Registrado"
                    registrar_auditoria(user["id"], accion, request)

                return user
            
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

    def login_user(self, user_data: UserLogin,request: Request) -> dict:
      try:
        with get_cursor() as cursor:
            cursor.execute("SELECT id, username, password,role FROM usuarios WHERE username = %s", (user_data.username,))
            user = cursor.fetchone()
            
            if not user or not verify_password(user_data.password, user["password"]):
                raise HTTPException(status_code=401, detail="Credenciales inválidas")

            # Auditoria
            
            accion = "Inicio de sesión"
            registrar_auditoria(user["id"], accion, request)

            return {"id": user["id"], "username": user["username"],"role":user["role"]}
      except Exception as e:
         logger.error("Error al iniciar Sesion {}".format(e))
         raise
      
    def get_profile(self, user: dict) -> dict:
      
      try:  
        with get_cursor() as cursor:
            if user["role"] == "admin":
                cursor.execute(
                    "SELECT fullname, username, age, email, role FROM usuarios WHERE username = %s", (user["username"],)
                )
            else:
                cursor.execute(
                    "SELECT fullname, username, age, email FROM usuarios WHERE username = %s", (user["username"],)
                )
            user = cursor.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
            return user
      except Exception as e:
         logger.error("Error al ver Perfil {}".format(e))         
         raise
      
    def update_user(self,request:Request,update_user:UserUpdate,user:dict):

     try:
      with get_cursor() as cursor:

         cursor.execute("SELECT id,password FROM usuarios WHERE username = %s",(user["username"],))
         user_db = cursor.fetchone()
         
         if not user_db :
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

         if not verify_password(update_user.current_password,user_db["password"]):
            raise HTTPException(status_code=400,detail="Contraseña invalida")
        

        
         campos = update_user.model_dump(exclude_unset=True,exclude={"current_password"})

         

         

         if "new_password" in campos:
          
          campos["password"]= hash_password(campos.pop("new_password"))
         
         
         columnas = list(campos.keys())  
         valores = list(campos.values()) 
         
         set_sql = ", ".join([f"{col} = %s" for col in columnas])
         valores.append(user_db["id"])
         query = f"UPDATE usuarios SET {set_sql} WHERE id = %s"

         cursor.execute(query,valores)
         # Auditoria
            
         accion = "Modifico Datos"
         registrar_auditoria(user_db["id"], accion, request)

      return {"message":"Usuario Actualizado"}
     except Exception as e:
        logger.error("Error al actualizar usuario{}".format(e))        
        raise
     

    def delete_user(self,request:Request,user_delete:UserDelete,user:dict ) -> dict:
      try:
        with get_cursor() as cursor:
 
         cursor.execute("SELECT id,password FROM usuarios WHERE username = %s",(user["username"],))
         user_bd = cursor.fetchone()
         
         if not user_bd :
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

         if not verify_password(user_delete.password,user_bd["password"]):
            raise HTTPException(status_code=400,detail="Contraseña invalida")

         cursor.execute("DELETE FROM usuarios WHERE id =%s",(user_bd["id"],))
         # Auditoria
            
         accion = "Se Elimino Usuario"
         registrar_auditoria(user["id"], accion, request)

         message = {"Usuario":"Eliminado Exitosamente"}
         return message
      except Exception as e: 
         logger.error("Error al eliminar usuario{}".format(e))
         raise