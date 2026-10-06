from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from .schemas import UserCreate, UserRegisterResponse, UserResponse
from .service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .utils import create_access_token, decode_access_token

auth_router = APIRouter()

@auth_router.post(
    "/signup", 
    response_model=UserRegisterResponse, 
    status_code=status.HTTP_201_CREATED
)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    user_service = UserService(session=session)
    
    # 1. Check if user exists and raise HTTPException directly
    if await user_service.user_exists(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User with this email already exists."
        )
    
    # 2. Create user and return success dictionary matching UserRegisterResponse schema
    new_user = await user_service.create_user(user_data)
    return {"message": "User registered successfully", "user": new_user}

@auth_router.post("/login")
async def login():
   pass

@auth_router.get("/logout")
async def logout():
    return {"message": "Logout endpoint"}
