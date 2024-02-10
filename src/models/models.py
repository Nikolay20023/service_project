from sqlalchemy import Enum, Column, Integer, String, DateTime, func, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from enum import Enum as PythonEnum
import uuid


from models.base import Base


user_service = Table(
    "user_service",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE")),
    Column("service_id", ForeignKey("services.id", ondelete="CASCADE")),
    Column("price", Integer, nullable=False)
)


class UserRole(PythonEnum):
    ADMIN = "admin"
    User = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(length=128), unique=True, nullable=False)
    email = Column(String, unique=True, index=True)
    first_name = Column(String(length=128))
    last_name = Column(String(length=128))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(),
                        onupdate=func.current_timestamp())
    role = Column(Enum(UserRole, name="user_role"), default=UserRole.User)
    hashed_password = Column(String())
    services = relationship(
        "Service", secondary=user_service, back_populates="users", lazy="selectin"
    )

    def get_full_name(self):
        return f"{self.last_name} + {self.first_name}"


class Service(Base):
    __tablename__ = "services"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(length=256), nullable=False, unique=True)
    discription = Column(String(length=256))
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(),
                        onupdate=func.current_timestamp())
    users = relationship(
        "User", secondary=user_service, back_populates="services", lazy="selectin"
    )
    price = Column(Integer, nullable=False)
