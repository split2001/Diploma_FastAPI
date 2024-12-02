from sqlalchemy import Column, Integer, String, Boolean
from app.backend.db import Base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CreateTable
from slugify import slugify


class User(Base):  # модель User, наследованная от ранее написанного Base
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    books = relationship('Book', back_populates='user', cascade='save-update, merge, delete, delete-orphan')
    # объект связи с таблицей Book
    # back_populates содержит в себе название объекта для связи


print(CreateTable(User.__table__))
