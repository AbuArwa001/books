from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from .schemas import UserCreate, UserRegisterResponse, UserResponse, UserLoginModel
from .service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .utils import create_access_token, decode_access_token, verify_password
from fastapi.responses import JSONResponse
from datetime import timedelta

auth_router = APIRouter()
REFRESH_TOKEN_EXPIRE_DAYS = 2
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
async def login(user_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    password = user_data.password
    uservice_service = UserService(session)
    user = await uservice_service.get_user_by_email(email)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    access_token = create_access_token(data={
        "email": email,
        "user_id": str(user.uid)
        })
    refresh_token = create_access_token(data={
        "email": email,
        "user_id": str(user.uid)
        }, 
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        refresh=True)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_verified": user.is_verified,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "uid": str(user.uid)
            }
        }
    )
@auth_router.post("/logout")
async def logout():
    return {"message": "Logout endpoint"}
