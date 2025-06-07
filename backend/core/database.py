# Escritorio/GIT/backend/db/db.py
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
    except Exception as E:
        if conn:
            conn.rollback()
        raise E 
    finally:
        if cursor: 
            cursor.close()
        if conn:
            conn.close()

def get_connection():
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.commit()
        return conn
        
    except Exception as e:
        conn.rollback()
        raise e
