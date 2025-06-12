#Escritorio/GIT/backend/main.py
from fastapi import FastAPI,Depends
from backend.routers import users,products,cart
from backend.middleware.logger_middleware import LoggingMiddleware
from backend.utils.auth import create_guest
from backend.repositories.user_repository_postgres import UserRepositoryPostgres
from backend.service.user_service import UserService

user_repo = UserRepositoryPostgres()
user_service = UserService(user_repo)

app = FastAPI()
app.add_middleware(LoggingMiddleware)
app.include_router( users.router)
app.include_router(products.router)
app.include_router(cart.router)
@app.post("/")
def sesion_guest():
    token = create_guest()
    return token
