
from backend.schemas.stock_schema import Stock
from backend.interfaces.stock_interface import IStockService
from backend.interfaces.stock_repository_interface import IStockRepository
from backend.core.database import get_cursor
class StockService(IStockService):
    def __init__(self,repository_stock:IStockRepository):
        self.repository_stock = repository_stock

    def insert_stock(self,stock:Stock):
        try:
            with get_cursor() as cursor:

                self.repository_stock.add(cursor,stock)
                return {"Stock agregado"}
        except Exception as e:
            raise    