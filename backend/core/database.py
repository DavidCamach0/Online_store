# Escritorio/GIT/backend/core/database.py
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import os 
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL =os.getenv("DATABASE_URL_LOCAL")
@contextmanager
def get_cursor():

    
    conn = psycopg2.connect(DATABASE_URL)
    
    try:
     
        

        cursor = conn.cursor(cursor_factory=RealDictCursor)

        yield cursor

        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e 
    finally:
        if cursor: 
            cursor.close()
        if conn:
            conn.close()

@contextmanager
def get_connection():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        yield conn  # devolvés la conexión para ser usada afuera
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()
