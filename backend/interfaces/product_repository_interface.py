from abc import abstractmethod,ABC
from backend.schemas.product_schema import ProductNew,Product


class IProductRepository(ABC):
    @abstractmethod
    def create_product(self,product:ProductNew):
        pass