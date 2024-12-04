from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.backend.db import Base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CreateTable
from app.models import user
from slugify import slugify
from app.models.association import UserBook


class Book(Base):  # модель Task, наследованную от ранее написанного Base
    __tablename__ = 'books'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    author = Column(String)
    genre = Column(String)
    # user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True, index=True)
    # ForeignKey внешний ключ на id из таблицы 'users'
    # ondelete='CASCADE' для удаления tasks при удалении users

    # объект связи с таблицей User
    user_books = relationship('UserBook',  back_populates='book')
    users = relationship('User', secondary='user_book', back_populates='books')
    # back_populates содержит в себе название объекта для связи


# print(CreateTable(Book.__table__))
