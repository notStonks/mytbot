from fastapi import FastAPI
from api.routers import users, medicines

app = FastAPI()

app.include_router(users.router)
app.include_router(medicines.app)


