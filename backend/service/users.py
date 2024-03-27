from service.repository import RepositoryDB
from schema.user import UserCreate, UserUpdate, UserService, UserServiceUpdate
from schema.service import ServiceCreate, ServiceUpdate
from models.models import User, Service, user_service


class RepositoryUser(RepositoryDB[User, UserCreate, UserUpdate]):
    pass


class RepositoryService(RepositoryDB[Service, ServiceCreate, ServiceUpdate]):
    pass


class RepositoryUserService(RepositoryDB[user_service, UserService, UserServiceUpdate]):
    pass


user_crud = RepositoryUser(User)

service_crud = RepositoryService(Service)

user_service_crud = RepositoryUserService(user_service)
