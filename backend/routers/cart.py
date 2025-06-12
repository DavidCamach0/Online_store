from fastapi import APIRouter,HTTPException,Depends,Request
from backend.utils.auth import verify_token,require_role
from backend.schemas.cart_schema import ItemCart
from backend.repositories.cart_repository_postgres import CartRepositoryPostgres
from backend.service.cart_service import CartService

router = APIRouter(prefix="/cart",tags=["cart"])

repo = CartRepositoryPostgres()
cart_service = CartService(repo)

@router.get("/",dependencies=[Depends(verify_token)])
async def cart(request:Request,user:dict = Depends(require_role(["admin","user"]))):
    try:
        cart = cart_service.show_cart(request,user)
        return {"message":cart}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
   


@router.post("/add",dependencies=[Depends(verify_token)])
async def cart(request:Request,item:ItemCart,user:dict = Depends(require_role(["admin","user"]))):
    try:
        
        message = cart_service.add_cart(request,item,user)
        return message
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
