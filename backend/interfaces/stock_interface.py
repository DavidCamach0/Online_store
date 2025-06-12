from abc import ABC,abstractmethod
from backend.schemas.stock_schema import Stock


class IStockService(ABC):

    @abstractmethod
    def insert_stock(self,stock:Stock):
        pass