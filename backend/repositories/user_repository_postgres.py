# repositories/user_repository_postgres.py
from backend.interfaces.user_repository_interface import IUserRepository
from backend.core.database import get_cursor,get_connection
from psycopg2.extras import RealDictCursor
from backend.utils.hash import hash_password
from datetime import datetime, timezone

class UserRepositoryPostgres(IUserRepository):
    def create_user(self, user_data):
        with get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            hashed_pwd = hash_password(user_data.password)

            cursor.execute(
                """
                INSERT INTO users (fullname, username, email, age, password, role, state, registration_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, username, email
                """,
                (
                    user_data.fullname,
                    user_data.username,
                    user_data.email,
                    user_data.age,
                    hashed_pwd,
                    user_data.role,
                    "pendiente",
                    datetime.now(timezone.utc)
                )
            )

            user = cursor.fetchone()
            cursor.close()
            conn.commit()
            return user

    def get_user_by_email(self, email):
        with get_cursor() as cursor:
            
            cursor.execute("""UPDATE users SET state = 'confirmado' WHERE email = %s 
                           RETURNING id, username, email""", (email,))
            user = cursor.fetchone()
            return user

    def login_user(self, user_data):
        with get_cursor() as cursor:
            cursor.execute("SELECT id, username, password,role FROM users WHERE username = %s", (user_data.username,))
            user = cursor.fetchone()
            return user
        

    def get_me(self,user):

         with get_cursor() as cursor:
            
            cursor.execute(
                    "SELECT fullname, username, age, email, role FROM users WHERE username = %s", (user["username"],)
                )
            user = cursor.fetchone()
         return user  
    
    def get_user_by_username(self,username) -> dict | None:
        with get_cursor() as cursor:
            cursor.execute("SELECT id, password FROM users WHERE username = %s", (username["username"],))
            return cursor.fetchone()
        

    def update_user(self,user_id: int, campos: dict):
        with get_cursor() as cursor:
            columnas = list(campos.keys())
            valores = list(campos.values())

            set_sql = ", ".join([f"{col} = %s" for col in columnas])
            valores.append(user_id)

            query = f"UPDATE users SET {set_sql} WHERE id = %s"
            cursor.execute(query, valores)
 
    def delete_user(self,id:int):
        with get_cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id =%s",(id,))

        



       