from backend.core.database import get_cursor,get_connection,RealDictCursor
from backend.interfaces.stock_repository_interface import IStockRepository



class StockRepositoryPostgres(IStockRepository):

    def add(self, cursor, stock):

        cursor.execute("INSERT INTO stock (product_id,quantity) VALUES (%s,%s)",(stock.product_id,stock.quantity))

