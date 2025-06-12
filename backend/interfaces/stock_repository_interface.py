from abc import abstractmethod,ABC


class IStockRepository(ABC):
    @abstractmethod
    def add(self,cursor,stock):
        pass