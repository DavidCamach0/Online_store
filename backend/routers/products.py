#/Escritorio/GIT/backend/routers/products.py
from fastapi import APIRouter,Depends
from backend.utils.auth import  verify_token,require_role
from backend.schemas.models import Product
from backend.core.database import get_cursor,get_connection
from backend.utils.logger import get_logger
from backend.service.product_service import ProductService
from typing import Optional
router = APIRouter()

logger = get_logger(__name__)

product_service = ProductService()

@router.get("/",dependencies = [Depends(verify_token)])
async def products(filter:Product,role:dict = Depends(require_role(["invitado","user","admin"]))):
    try:
        
        print("bienvenindo",role["role"])
        return product_service.show_product(filter)
       
    except Exception as e:
        logger.error(e)        

