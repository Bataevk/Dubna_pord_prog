from __future__ import annotations
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

user_connections = Table(
    "user_connections",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("dbconnection_id", ForeignKey("dbconnection.id")),
)
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("role_id", ForeignKey("roles.id")),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    phonenumber = Column(String(100), nullable=True)
    telegrm_id = Column(Integer, nullable=True)
    user_roles = relationship("Role", secondary= user_roles, backref="roles", lazy='subquery')
    user_connections = relationship("DbConnection", secondary = user_connections, backref="dbconnection",lazy='subquery')
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True ,autoincrement=True)
    name = Column(String(100), nullable=False)
    managed_user = Column(Boolean, nullable=False)
    managed_roles= Column(Boolean, nullable=False)
    managed_links= Column(Boolean, nullable=False)
    managed_active_db = Column(Boolean, nullable=False)
    managed_logs = Column(Boolean, nullable=False)


class DbConnection(Base):
    __tablename__ = "dbconnection"
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(100), nullable=True)
    host = Column(String(100), nullable=True)
    port = Column(String(100), nullable=True)
    username = Column(String(100), nullable=True)
    userpassword = Column(String(100), nullable=True)

class Auth:
    __tablename__ = "auth"
    user_id = Column(Integer, primary_key=True)
    date_time = Column(DateTime, nullable=False)

