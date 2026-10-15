from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.auth.routes import auth_router
from src.books.routes import book_router
from src.tags.routes import tag_router
from src.review.routes import review_router
from src.db.main import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server is starting....")
    await init_db()
    yield
    print("Sever Has been Stopped")


version = "v1"

app = FastAPI(
    title="Book API",
    description="A Book Review Web Service",
    version=version,
)
app.include_router(
    book_router, prefix=f"/api/{version}/books", tags=["Books"]
)
app.include_router(
    auth_router, prefix=f"/api/{version}/auth", tags=["Auth"]
)
app.include_router(
    tag_router, prefix=f"/api/{version}/tags", tags=["Tags"]
)
app.include_router(
    review_router, prefix=f"/api/{version}/reviews", tags=["Reviews"]
)