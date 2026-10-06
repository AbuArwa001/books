from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Server is starting....")
    await init_db()
    yield
    print(f"Sever Has been Stopped")
version = "v1"

app = FastAPI(
    title="Book API",
    description="A Book Review Web Service",
    version= version,
    lifespan=lifespan
)
app.include_router(book_router, prefix=f"/api/{version}/books", tags=['Books'])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['Auth'])
