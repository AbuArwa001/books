from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.tags.schemas import Tags, TagsSchema, TagsSchema


class TagsService(BaseModel):
    def __init__(self, session: AsyncSession):
         self.session = session

    def create_tag(self, tag_data: TagsSchema):
        tag = Tags(**tag_data.model_dump())
        self.session.add(tag)
        self.session.commit()
        self.session.refresh(tag)
        return tag
    def get_all_tags(self):
        tags = self.session.query(Tags).all()
        return tags
    def get_tag(self, tag_id: int):
        tag = self.session.query(Tags).filter(Tags.id == tag_id).first()
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        return tag
    def update_tag(self, tag_id: int, tag_data: TagsSchema):
        tag = self.get_tag(tag_id)
        for key, value in tag_data.model_dump().items():
            setattr(tag, key, value)
        self.session.commit()
        self.session.refresh(tag)
        return tag
    def delete_tag(self, tag_id: int):
        tag = self.get_tag(tag_id)
        self.session.delete(tag)
        self.session.commit()
