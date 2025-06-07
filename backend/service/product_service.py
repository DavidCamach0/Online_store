# Escritorio/GIT/backend/service/product_service.py
from backend.core.database import get_cursor,get_connection
from fastapi import HTTPException, status,Depends,Request
from backend.schemas.models import Product
from backend.utils.logger import get_logger
from backend.utils.audit import registrar_auditoria
from psycopg2.extras import RealDictCursor
from typing import Optional
logger = get_logger(__name__)



class ProductService:
    def show_product(self,filter:Product):
        try:
            with get_cursor() as cursor:
                
                if filter.category is None:    
                    cursor.execute("SELECT * FROM products")
                    product = cursor.fetchall()
                else:
                    cursor.execute("SELECT * FROM products WHERE category = %s",(filter.category,))
                    product = cursor.fetchall()

                return product
        except Exception as e:
            logger.error(e)    
