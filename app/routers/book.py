from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import *
from app.shemas import CreateUser, UpdateUser, CreateBook, UpdateBook
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify
from app.routers import user

router = APIRouter(prefix='/book', tags=['book'])


@router.get('/')
async def all_books(db: Annotated[Session, Depends(get_db)]):  # подключается к базе данных в момент обращения при
    # помощи функции get_db
    books = db.execute(select(Book)).scalars().all()
    return books  # возвращать список всех книг из БД


@router.get('/book_id')
async def book_by_id(db: Annotated[Session, Depends(get_db)], book_id: int):  # подключается к базе данных в момент
    # обращения при помощи функции get_db:
    book = db.scalar(select(Book).where(Book.id == book_id))
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Книга не найдена'
        )
    else:
        return book


@router.post('/create')
async def create_book(db: Annotated[Session, Depends(get_db)], create_book: CreateBook, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )
    db.execute(insert(Book).values(
                                    title=create_book.title,
                                    description=create_book.description,
                                    author=create_book.author,
                                    genre=create_book.genre,
                                    completed=create_book.completed
    ))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update')
async def update_book(db: Annotated[Session, Depends(get_db)], book_id: int, update_book:  UpdateBook):
    book = db.scalar(select(Book).where(Book.id == book_id))
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Книга не найдена'
        )
    db.execute(update(Book).where(Book.id == book_id).values(
        title=update_book.title,
        description=update_book.description,
        author=update_book.author,
        genre=update_book.genre,
        completed=False
    ))

    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Книга успешно обновлена!'}


@router.delete('/delete')
async def delete_book(db: Annotated[Session, Depends(get_db)], book_id: int):
    # подключается к базе данных в момент обращения при помощи функции get_db
    book = db.scalar(select(Book).where(Book.id == book_id))
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Книга не найдена'
        )
    db.execute(delete(Book).where(Book.id == book_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Книга успешно удалена'}
