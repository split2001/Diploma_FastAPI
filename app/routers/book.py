from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models.book import Book
from app.models.user import User
from app.shemas import CreateUser, UpdateUser, CreateBook, UpdateBook, UpdateBookStatus
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify
from app.routers.user import *

router = APIRouter(prefix='/book', tags=['book'])


@router.get('/')
async def all_books(db: Annotated[Session, Depends(get_db)]):  # подключается к базе данных в момент обращения при
    # помощи функции get_db
    books = db.query(Book).all()
    return books  # возвращать список всех книг из БД


@router.get('/book_author')
async def book_by_author(db: Annotated[Session, Depends(get_db)], book_author: str): # подключается к базе данных в момент
    # обращения при помощи функции get_db:
    books = db.query(Book).filter(Book.author == book_author).all()
    if books is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Книга не найдена'
        )
    else:
        return books


@router.get('/book_genre')
async def book_by_genre(db: Annotated[Session, Depends(get_db)], book_genre: str): # подключается к базе данных в момент
    # обращения при помощи функции get_db:
    books = db.query(Book).filter(Book.genre == book_genre).all()
    if books is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Книга не найдена'
        )
    else:
        return books


@router.post('/create')
async def create_book(db: Annotated[Session, Depends(get_db)], title: str, description: str,
                      author: str, genre: str):
    existing_book = db.query(Book).filter(Book.title == title).first()
    if existing_book is None:
        new_book = Book(title=title, description=description, author=author, genre=genre, completed=False)
        db.add(new_book)
        db.commit()
        return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Такая книга уже существует')


@router.put('/update_book')
async def update_book(db: Annotated[Session, Depends(get_db)], book_id: int, update_book: UpdateBook):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Книга не найдена'
        )
        # Обновляем поля книги
    if update_book.title is not None:
        book.title = update_book.title
    if update_book.description is not None:
        book.description = update_book.description
    if update_book.author is not None:
        book.author = update_book.author
    if update_book.genre is not None:
        book.genre = update_book.genre
    if update_book.completed is not None:
        book.completed = False
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Книга успешно обновлена!'}


@router.put('/update_book_status')
async def update_book_status(db: Annotated[Session, Depends(get_db)], book_id: int, update_book_status: UpdateBookStatus):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Книга не найдена'
        )
    if update_book_status.completed is not None:
        book.completed = True
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Статус успешно обновлен!'}


@router.put('/usersbook')
async def user_to_book(db: Annotated[Session, Depends(get_db)], user_id: int, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Книга не найдена'
        )
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )
    if book not in user.books:
        user.books.append(book)
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'Книга успешно добавлена'}


@router.delete('/delete')
async def delete_book(db: Annotated[Session, Depends(get_db)], book_id: int):
    # подключается к базе данных в момент обращения при помощи функции get_db
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Книга не найдена'
        )
    db.delete(book)
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Книга успешно удалена'}
