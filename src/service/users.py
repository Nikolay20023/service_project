from service.repository import RepositoryDB
from schema.user import UserCreate, UserUpdate
from schema.service import ServiceDB, ServiceCreate, ServiceUpdate
from models.models import User, Service


class RepositoryUser(RepositoryDB[User, UserCreate, UserUpdate]):
    pass


class RepositoryService(RepositoryDB[Service, ServiceCreate, ServiceUpdate]):
    pass


user_crud = RepositoryUser(User)

service_crud = RepositoryService(Service)
