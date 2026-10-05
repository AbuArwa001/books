from sqlmodel import create_engine, text
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config

engine = AsyncEngine(
    create_engine(
    url=Config.DATABASE_URL,
    echo=True
))

async def init_db():
    async with engine.begin() as conn:
        statement = text("SELECT 'hello';")

        result = await conn.execute(statement)

# ALTER USER khalifah WITH PASSWORD 'Khalif01#2023';
# \q
# CREATE DATABASE bookly_db OWNER khalifah;
        print(result.all)

         