from fastapi import APIRouter
from .schemas import UserCreate, UserLogin

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@auth_router.post("/signup")
async def register(user_data: UserCreate):
    return {"message": "Register endpoint"}

@auth_router.get("/login")
async def login():
    return {"message": "Login endpoint"}

@auth_router.get("/logout")
async def logout():
    return {"message": "Logout endpoint"}
