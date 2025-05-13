import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import os 
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL =os.getenv("DATABASE_URL")
@contextmanager
def get_cursor():

    
    conn = psycopg2.connect(DATABASE_URL)
    
    try:
     
        print("conexion Exitosa")

        cursor = conn.cursor(cursor_factory=RealDictCursor)

        yield cursor

        conn.commit()
    except Exception as E:
        if conn:
            conn.rollback()
        raise E 
    finally:
        if cursor: 
            cursor.close()
        if conn:
            conn.close()

'''def probar():

    with get_cursor() as cursor:

        cursor.execute("SELECT * FROM usuarios")
        result = cursor.fetchall()

    print(result)    


probar()'''