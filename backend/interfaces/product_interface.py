from abc import abstractmethod,ABC
from fastapi import Request
from backend.schemas.product_schema import Product



class IProductService(ABC):

    
    @abstractmethod
    def create_product(self,request:Request,product:Product,user:dict):
        pass

   

