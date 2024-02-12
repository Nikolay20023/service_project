from typing import Any, Dict, List, Generic, Optional, Type, TypeVar, Union
import logging
import uuid
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from service.base import Repository
from models.base import Base
from core.logger import LOGGING


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class RepositoryDB(Repository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]) -> None:
        self._model = model

    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self._model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        return db_obj

    async def get(self, db: AsyncSession, id: uuid.UUID | None = None, username: str | None = None) -> Optional[ModelType]:
        if not username:
            statement = select(self._model).where(self._model.id == id)
            results = await db.execute(statement=statement)
            return results.scalar_one_or_none()

        statement = select(self._model).where(self._model.username == username)
        results = await db.execute(statement=statement)
        db_obj = results.scalar_one_or_none()
        return db_obj

    async def get_multi(
            self, db: AsyncSession, *, offset=0, limit=100
    ):
        statement = select(self._model).offset(offset).limit(limit)
        results = await db.execute(statement=statement)
        return results.scalars()

    async def upgrade(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            for key, value in obj_in.items():
                setattr(db_obj, key, value)
        else:
            update_data = jsonable_encoder(obj_in)
            for key, value in update_data.items():
                setattr(db_obj, key, value)

        await db.commit()
        return db_obj

    async def delete(
        self,
        db: AsyncSession,
        *,
        id: uuid.UUID
    ):
        statement = select(self._model).where(self._model.id == id)
        results = await db.execute(statement=statement)
        db_obj = results.scalar()
        if db_obj:
            await db.delete(db_obj)
            await db.commit()

    async def insert(self, db: AsyncSession, *, obj_in: CreateSchemaType):
        obj_in_data = jsonable_encoder(obj_in)
        statement = self._model.insert().values(**obj_in_data)
        result = await db.execute(statement=statement)

        await db.commit()

        return result
