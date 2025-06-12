#/Escritorio/GIT/backend/routers/products.py
from fastapi import APIRouter,Depends,Request,HTTPException
from backend.utils.auth import  verify_token,require_role
from backend.schemas.product_schema import Product,ProductNew,ProductUpdate,ProductDelete,Filter
from backend.schemas.stock_schema import Stock
from backend.repositories.product_repository_postgres import ProductRepositoryPostgres
from backend.repositories.stock_repository_postgres import StockRepositoryPostgres
from backend.core.database import get_cursor,get_connection
from backend.utils.logger import get_logger
from backend.service.product_service import ProductService
from backend.service.stock_service import StockService
router = APIRouter()

logger = get_logger(__name__)

repo = ProductRepositoryPostgres()
product_service = ProductService(repo)

repo_stock = StockRepositoryPostgres()
stock_service = StockService(repo_stock)

@router.get("/",dependencies = [Depends(verify_token)])
async def products(filter:Filter,user:dict = Depends(require_role(["invitado","user","admin"]))):
    try:
        
        print("bienvenindo",user["role"])
        return product_service.show_product(filter)
       
    except Exception as e:
        logger.error(e)   

@router.post("/newProduct",dependencies = [Depends(verify_token)])   
async def new_product(request:Request,product:ProductNew,user:dict = Depends(require_role(["admin"]))):
    try:

        print("bienvenido ",user["role"])      
        
        product_id = product_service.create_product(request,product,user)  # Usa solo name, price, etc.
        stock = Stock(product_id=product_id,quantity= product.stock)

       
        p=stock_service.insert_stock(stock)
       
        return {"mensaje": "Producto agregado exitosamente"}
    except HTTPException as e:
        raise e  # Reenvía HTTPException con su status y detail
    except Exception as e:
        logger.error(f"Fallo inesperado en router: {e}")
        raise HTTPException(status_code=500, detail="Error inesperado al agregar el producto")

@router.put("/updateProduct",dependencies = [Depends(verify_token)])
async def update_product(request:Request,product:ProductUpdate,user:dict = Depends(require_role(["admin"]))):

    try:

        print("bienvenido",user["role"])
        message = product_service.update_product(request,product,user)
        return message
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500,detail= str(e))

@router.delete("/deleteProduct",dependencies = [Depends(verify_token)])
async def delete_product(request:Request,product:ProductDelete,user:dict = Depends(require_role(["admin"]))):

    try:

        print("bienvenido",user["role"])
        message = product_service.delete_product(request,product,user)
        return message
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500,detail= str(e))
