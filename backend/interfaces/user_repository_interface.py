# interfaces/user_repository_interface.py
from abc import ABC, abstractmethod
from backend.schemas.user_schema import UserCreate, UserLogin,UserDelete

class IUserRepository(ABC):

    @abstractmethod
    def create_user(self, user_data: UserCreate) -> dict:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> dict:
        pass

    @abstractmethod
    def login_user(self,user_data:UserLogin)-> dict:
        pass

    @abstractmethod
    def get_me(self,user:dict)-> dict:
        pass

    @abstractmethod
    def get_user_by_username(self,username):
        pass
    @abstractmethod
    def update_user(self, user_id: int, campos: dict):
        pass

    @abstractmethod
    def delete_user(self,password:UserDelete):
        pass
