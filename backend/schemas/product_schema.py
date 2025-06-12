
from pydantic import BaseModel
from typing import Optional

class Filter(BaseModel):
    
    name:Optional[str]= None
    price:Optional[float]= None
    category:Optional[str]= None

class ProductNew(BaseModel):
    name:str
    price:float
    description:str
    category:str
    stock:int    

class Product(BaseModel):
    name:str
    price:float
    description:str
    category:str    

class ProductUpdate(BaseModel):
    name:str
    price:Optional[float]= None
    description:Optional[str]= None

class ProductDelete(BaseModel):
    name:str 