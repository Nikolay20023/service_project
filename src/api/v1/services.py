import logging
from fastapi import APIRouter, Depends, status
from typing import Annotated
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from db.db import get_session
from schema.user import User
from schema.service import ServiceDB, ServiceCreate
from api.v1.users import get_current_user
from service.users import service_crud, user_crud
from core.logger import LOGGING


logging.basicConfig(level=logging.INFO,
                    format=LOGGING['formatters']['verbose']['format'])
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_service(
    service: ServiceCreate,
    db: AsyncSession = Depends(get_session),
):
    try:
        new_service = await service_crud.create(db=db, obj_in=service)
        logger.info(f"Succerfull create service :{new_service}")
    except SQLAlchemyError:
        raise
    return ServiceDB(**new_service.__dict__)


@router.get("/service/{id}", response_model=ServiceCreate)
async def get_service(
    id: uuid.UUID,
    user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_session),
):
    try:
        service = await service_crud.get(db=db, id=id)
        logger.warning(f"Service {service}")
    except TypeError as e:
        logger.warning(f"Error as {e}")
        raise e
    return ServiceCreate(**service.__dict__)


@router.get("/services/{username}")
async def get_multi_services(
    # user: Annotated[User, Depends(get_current_user)],
    username: str,
    db: AsyncSession = Depends(get_session),
):
    service = None
    try:
        user_db = await user_crud.get(db=db, username=username)
        service = user_db.services
    except Exception as ex:
        logger.info(f"{ex}")
    return service


@router.delete("/service/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    id: str,
    db: AsyncSession = Depends(get_session),
):
    try:
        await user_crud.delete(id=id, db=db)
    except Exception:
        raise Exception
    except ValueError as e:
        return
    return {
        "message": "Succerful delete"
    }


@router.patch("/service")
async def patch_service(
    db: AsyncSession = Depends(get_session)
):
    pass
