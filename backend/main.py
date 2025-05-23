
from fastapi import FastAPI
from backend.routers import users
from backend.middleware.logger_middleware import LoggingMiddleware


app = FastAPI()
app.add_middleware(LoggingMiddleware)
app.include_router( users.router )

@app.get("/")
def read_root():
   return {"message":"API activa"}
