from abc import ABC, abstractmethod
from fastapi import Request
from backend.schemas.user_schema import UserCreate, UserLogin, UserUpdate, UserDelete

class IUserService(ABC):

    @abstractmethod
    def register_user(self, request: Request, user_data: UserCreate) -> tuple:
        pass

    @abstractmethod
    def email_confirm(self, token: str) -> dict:
        pass

    @abstractmethod
    def login_user(self, user_data: UserLogin, request: Request) -> dict:
        pass

    @abstractmethod
    def get_profile(self, user: dict) -> dict:
        pass

    @abstractmethod
    def update_user(self, request: Request, update_user: UserUpdate, user: dict) -> dict:
        pass

    @abstractmethod
    def delete_user(self, request: Request, user_delete: UserDelete, user: dict) -> dict:
        pass
