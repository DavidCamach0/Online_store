from abc import ABC,abstractmethod


class ICartService(ABC):

    @abstractmethod
    def show_cart(self):
        pass
    
    @abstractmethod
    def add_cart(self):
        pass
