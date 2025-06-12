# Escritorio/GIT/backend/service/product_service.py
from backend.core.database import get_cursor,get_connection
from fastapi import HTTPException, status,Depends,Request
from backend.schemas.product_schema import Product,ProductUpdate
from backend.interfaces.product_interface import IProductService
from backend.interfaces.product_repository_interface import IProductRepository
from backend.utils.logger import get_logger
from backend.utils.audit import registrar_auditoria
from psycopg2 import IntegrityError
logger = get_logger(__name__)



class ProductService(IProductService):
    def __init__(self,product_repository:IProductRepository):
        self.product_repository = product_repository
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
    
    def create_product(self, request, product:Product, user):
        try:
            with get_cursor() as cursor:
                product_id = self.product_repository.create_product(cursor,product)
                return product_id["id"]
           
        except IntegrityError as e:
            error_message = str(e)
           

            if "unique_product_name"  in error_message:
                raise HTTPException(status_code=400, detail="El producto ya está registrado")
        except Exception as e:
            logger.error(f"Error inesperado en el servicio creacion product: {e}")
            raise 
    
    def update_product(self,request,product:ProductUpdate,user:dict):
        try:
            with get_cursor() as cursor:
                
                id = self.product_repository.get_product(cursor,product.name)
                
                if not id  or id == None :
                    raise HTTPException(status_code=401,detail="El producto no fue Encontrado")
                
                campos = product.model_dump(exclude_unset=True,exclude={"name"})
                
                self.product_repository.update_product(cursor,campos,id["id"])

            return {"message: Producto Actualizado"}
        
        except Exception as e:
            logger.error(e)
            raise    

    def delete_product(self,request,product,user):
       try:
            with get_cursor() as cursor:
                
                id = self.product_repository.get_product(cursor,product.name)
                
                if not id  or id == None :
                    raise HTTPException(status_code=401,detail="El producto no fue Encontrado")
                
                
                
                self.product_repository.delete_product(cursor,id["id"])

            return {"message: Producto Eliminado"}
       except Exception as e:
            logger.error(e)
            raise    