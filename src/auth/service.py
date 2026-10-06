from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import User
from .schemas import UserCreate
from .utils import generate_password_hash


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await self.session.exec(statement)
        user = result.first()
        return user

    async def user_exists(self, email: str) -> bool:
        user = await self.get_user_by_email(email)
        return True if user else False

    async def create_user(self, user_data: UserCreate) -> User:
        user_data_dict = user_data.model_dump(exclude={"password"})
        new_user = User(
            **user_data_dict,
            password_hash=generate_password_hash(user_data.password),
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
