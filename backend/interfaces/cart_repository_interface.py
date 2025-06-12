from abc import abstractmethod,ABC
#from backend.schemas.cart_schema import ItemCart


class ICartRepository(ABC):
    @abstractmethod
    def add_product(self,cursor,product,cart_id):
        pass