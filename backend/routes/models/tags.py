from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import update, delete

from auth import TSession
from data_base.schema import (
    TagResponse,
    CreateTagRequest,
    UpdateTagRequest)
from data_base.models import Tag, Emergency


tags_router = APIRouter(prefix='/tags', tags=['Tags',])


@tags_router.post('/create', response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(form: CreateTagRequest, session: TSession) -> TagResponse:
    title = form.title
    stmt = select(Tag).filter_by(title=title)
    result = await session.execute(stmt)
    tag = result.scalars().first()

    if tag is not None:
        raise HTTPException(
            status_code=409,
            detail=f'Tag.title=`{title}` is already exists.'
        )

    emergencies_ids = form.emergencies_ids
    stmt = select(Emergency).where(Emergency.id.in_(emergencies_ids))
    result = await session.execute(stmt)
    emergencies = result.scalars().all()

    new_tag = Tag(
        title=title,
        emergencies=emergencies
    )
    session.add(new_tag)
    await session.commit()

    return TagResponse(
        id=new_tag.id,
        title=new_tag.title
    )


@tags_router.put('/update/{tag_id}', status_code=status.HTTP_201_CREATED)
async def update_tag(form: UpdateTagRequest, session: TSession) -> None:
    tag_id = form.tag_id
    fields = form.fields

    stmt = update(Tag).where(Tag.id==tag_id).values(**fields)
    await session.execute(stmt)
    await session.commit()


@tags_router.delete('/delete/{tag_id}', status_code=status.HTTP_200_OK)
async def delete_tag(tag_id: int, session: TSession) -> None:
    stmt = delete(Tag).where(Tag.id==tag_id)
    await session.execute(stmt)
    await session.commit()


@tags_router.get('/{tag_id}', response_model=TagResponse)
async def get_tag(tag_id: int, session: TSession) -> TagResponse:
    stmt = select(Tag).filter_by(id=tag_id)
    result = await session.execute(stmt)
    tag = result.scalars().first()

    if tag is None:
        raise HTTPException(
            status_code=404,
            detail=f'Tag.id={tag_id} is not already exists!'
        )

    return TagResponse(
        id=tag.id,
        title=tag.title
    )
