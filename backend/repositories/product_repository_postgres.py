#/Escritorio/GIT/backend/repositories/product_repository_postgres.py
from backend.core.database import get_cursor,get_connection,RealDictCursor
from backend.interfaces.product_repository_interface import IProductRepository



class ProductRepositoryPostgres(IProductRepository):
    def create_product(self,cursor,product):
     
        cursor.execute("""INSERT INTO products (name,price,description,category)
                         VALUES (%s,%s,%s,%s) RETURNING id 
                       """,(product.name,product.price,product.description,product.category))
        return cursor.fetchone()
    def get_product(self,cursor,product):
        
        cursor.execute("Select id from products Where name = %s",(product,))
        return cursor.fetchone()
    
    def update_product(self,cursor,product,id):
            columnas = list(product.keys())
            valores = list(product.values())

            set_sql = ", ".join([f"{col} = %s" for col in columnas])
            valores.append(id)

            query = f"UPDATE products SET {set_sql} WHERE id = %s"
            cursor.execute(query, valores)
   
    def delete_product(self,cursor,id):
         
         cursor.execute("Delete from products Where id = %s",(id,))