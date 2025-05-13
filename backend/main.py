
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from backend.models import User, User_delete, User_update
from backend.db import get_cursor
from backend.utils import password_hash, verify_password
from backend.auth import create_token, verify_token
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()


def current_user(user = Depends(verify_token)):
   
   if not user or user == None:
        raise HTTPException(status_code=400, detail="Aun no ha Iniciado Sesion")
   return user

@app.get("/")
def read_root():
   return {"message":"API activa"}

@app.post("/Register")
async def Register(user:User):
    try:
        with get_cursor() as cursor:
            cursor.execute('SELECT username FROM usuarios WHERE username = %s',(user.username,))

            if cursor.fetchone():
             raise HTTPException(status_code=400, detail="El usuario ya existe")

            cursor.execute('SELECT email FROM usuarios WHERE email = %s',(user.email,))

            if cursor.fetchone():
             raise HTTPException(status_code=400, detail="El email ya tiene una cuenta asociada")

            cursor.execute('INSERT INTO usuarios (fullname,username,email,age,password) VALUES (%s,%s,%s,%s,%s)',
                           (user.fullname,user.username,user.email,user.age,password_hash(user.password)))
            return {"message": "Usuario registrado correctamente"}  
    except Exception as E:
       raise HTTPException(status_code=500, detail=str(E))
    

@app.post("/login")   
async def login(user: OAuth2PasswordRequestForm = Depends() ):
   
   try:
      with get_cursor() as cursor:
        cursor.execute("SELECT username,password FROM usuarios WHERE username = %s",(user.username,))
        user_db = cursor.fetchone()
        
        if not user_db:
           raise HTTPException(status_code=400,detail="usuario no existente")
 
        password_db =user_db["password"]
         
        user_db = dict(user_db)
        print(user_db)
        if not verify_password(user.password,password_db):
           raise HTTPException(status_code=400,detail="Contraseña Incorrecta")
        a = create_token({"sub":user_db["username"]})
        
        return {"message":"Inision de sesion Exitosa","datos":user_db,"token":a} 
   except Exception as e:     
      raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/me")
async def me(user: str = Depends(current_user)):
   
   with get_cursor() as cursor:
      cursor.execute("SELECT fullname,username,age,email FROM usuarios WHERE username = %s ",(user,))
      user = cursor.fetchone()
      return user
   

@app.put("/mi-perfil")
async def update(update_user:User_update,user:str = Depends(current_user)):

    try:   


      with get_cursor() as cursor:

         cursor.execute("SELECT id,password FROM usuarios WHERE username = %s",(user,))
         user_bd = cursor.fetchone()
         
         if not user_bd :
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

         if not verify_password(update_user.current_password,user_bd["password"]):
            raise HTTPException(status_code=400,detail="Contraseña invalida")


        
         campos = update_user.model_dump(exclude_unset=True,exclude={"current_password"})

         

         

         if "new_password" in campos:
          
          campos["password"]= password_hash(campos.pop("new_password"))
         
         
         columnas = list(campos.keys())  
         valores = list(campos.values()) 
         
         set_sql = ", ".join([f"{col} = %s" for col in columnas])
         valores.append(user_bd["id"])
         query = f"UPDATE usuarios SET {set_sql} WHERE id = %s"

         cursor.execute(query,valores)

      return {"usuario":"actualizado"}
    except Exception as E:
       raise HTTPException(status_code=500, detail=str(E))
    
         
@app.delete("/delete-account")
async def deleteUser(user:User_delete,username:str = Depends(current_user)):

   try:
      with get_cursor() as cursor:
 
         cursor.execute("SELECT id,password FROM usuarios WHERE username = %s",(username,))
         user_bd = cursor.fetchone()

         
         if not user_bd :
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

         if not verify_password(user.password,user_bd["password"]):
            raise HTTPException(status_code=400,detail="Contraseña invalida")

         cursor.execute("DELETE FROM usuarios WHERE id =%s",(user_bd["id"],))

         return {"Usuario":"Eliminado Exitosamente"}



   except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))



  