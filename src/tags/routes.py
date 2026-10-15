from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.tags.schemas import TagsSchema
from src.tags.service import TagsService

router = APIRouter(prefix="/tags", tags=["Tags"])
# tag_service = TagsService(session=Depends(get_session))


@router.post("/", response_model=TagsSchema, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_data: TagsSchema,
    session: AsyncSession = Depends(get_session),
):
    service = TagsService(session)
    return service.create_tag(tag_data)

@router.get("/", response_model=list[TagsSchema])
async def get_all_tags(
    session: AsyncSession = Depends(get_session),
):
    service = TagsService(session)
    return service.get_all_tags()

@router.get("/{tag_id}", response_model=TagsSchema)
async def get_tag(
    tag_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = TagsService(session)
    return service.get_tag(tag_id)

@router.put("/{tag_id}", response_model=TagsSchema)
async def update_tag(
    tag_id: int,
    tag_data: TagsSchema,
    session: AsyncSession = Depends(get_session),
):
    service = TagsService(session)
    return service.update_tag(tag_id, tag_data)

@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: int,
    session: AsyncSession = Depends(get_session),
):
    service = TagsService(session)
    return service.delete_tag(tag_id)