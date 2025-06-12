from fastapi import HTTPException,Request,Depends
from backend.interfaces.cart_interface import ICartService
from backend.repositories.cart_repository_postgres import CartRepositoryPostgres
from backend.core.database import get_cursor
from backend.schemas.cart_schema import ItemCart

class CartService(ICartService):

    def __init__(self,repository:CartRepositoryPostgres):
        self.repository = repository


    def show_cart(self,request:Request,user:dict):
        try:
           with get_cursor() as cursor:
                
                cart_id = self.repository.get_cart_id(cursor,user["id"])
                
                if not cart_id or cart_id == None:
                    
                    self.repository.new_cart(cursor,user["id"])

                cart = self.repository.show_my_cart(cursor,user["id"])

                if cart == None:
                    cart = "Carrito Vacio"

                return cart

        except Exception as e:
            raise 
        

    def add_cart(self,request:Request,item:ItemCart,user:dict):
        try:
            with get_cursor() as cursor:
                print("1")
                cart_id = self.repository.get_cart_id(cursor,user["id"])
                print(cart_id)
                if not cart_id or cart_id == None:
                    
                    cart_id = self.repository.new_cart(cursor,user["id"])
                
                self.repository.add_product(cursor,item,cart_id["id"])
            return{"producto: agrado al carrito de compras"}        
        except Exception as e:
            raise        


        