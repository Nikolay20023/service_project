import logging
from fastapi import APIRouter, Depends, status
from typing import Annotated
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from db.db import get_session
from schema.user import User, UserService
from schema.service import ServiceDB, ServiceCreate, ServiceUpdate
from api.v1.users import get_current_user
from service.users import service_crud, user_crud, user_service_crud


router = APIRouter()


@router.post("/service/create", status_code=status.HTTP_201_CREATED)
async def create_service(
    service: ServiceCreate,
    db: AsyncSession = Depends(get_session),
):
    try:
        new_service = await service_crud.create(db=db, obj_in=service)
    except SQLAlchemyError:
        raise
    except Exception as e:
        logging.info(f"Exception raise is {e}")
    return ServiceDB(**new_service.__dict__)


@router.get("/service_get/{id}", response_model=ServiceCreate)
async def get_service(
    id: uuid.UUID,
    user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_session),
):
    try:
        service = await service_crud.get(db=db, id=id)
    except TypeError as e:
        raise e
    return ServiceCreate(**service.__dict__)


@router.get("/services_get_list/{username}")
async def get_multi_services(
    user: Annotated[User, Depends(get_current_user)],
    username: str,
    db: AsyncSession = Depends(get_session),
):
    user_db = await user_crud.get(db=db, id=username)
    if user_db:
        return {
            "services": user
        }


@router.delete("/service_delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    await service_crud.delete(id=id, db=db)
    return


@router.patch("/service_update/{id}")
async def patch_service(
    id: uuid.UUID,
    data: ServiceUpdate,
    db: AsyncSession = Depends(get_session),
):
    try:
        service_obj = await service_crud.get(db=db, id=id)
        service = await service_crud.upgrade(db=db, db_obj=service_obj, obj_in=data)
    except AttributeError:
        return {"message": "Incorrectly typed id"}
    return ServiceUpdate(**service.__dict__)


@router.post("/user_service", status_code=status.HTTP_201_CREATED)
async def create_user_service(
    data: UserService,
    db: AsyncSession = Depends(get_session)
):
    try:
        service = await service_crud.get(db=db, id=data.service_id)
        data.price = service.price
        new_ent = await user_service_crud.insert(db=db, obj_in=data)
    except Exception:
        raise Exception

    return {
        "new": new_ent
    }
