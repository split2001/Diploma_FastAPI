from fastapi import APIRouter, Depends, status, HTTPException, Form, Request
from sqlalchemy.orm import Session
# # Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.shemas import CreateUser, UpdateUser
from app.models.user import User
from app.models.book import Book
# # Функции работы с записями.
from sqlalchemy import select, insert, delete, update
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
#  Функция создания slug-строки


templates = Jinja2Templates(directory='app/templates')

router = APIRouter(prefix='/user', tags=['user'])


# Создаем контекст для хэширования и проверки паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Функция для хэширования паролей
def hash_password(password: str):
    return pwd_context.hash(password)


# Функция для проверки пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):  # подключается к базе данных в момент обращения при
    # помощи функции get_db
    users = db.query(User).all()
    return users  # возвращать список всех пользователей из


@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):  # подключается к базе данных в момент
    # обращения при помощи функции get_db
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )
    else:
        return user


@router.get('/register')
async def register_form(request: Request):
    print('request object:', request)
    return templates.TemplateResponse('register.html', {'request': request})


@router.post('/register')
async def register(request: Request, db: Annotated[Session, Depends(get_db)], username: str = Form(),
                   password: str = Form(), firstname: str = Form(), lastname: str = Form(), age: int = Form()
                   ):  # подключается к базе данных
    # в момент обращения при помощи функции get_db
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    hashed_password = hash_password(password)
    new_user = User(username=username, password=hashed_password, firstname=firstname, lastname=lastname, age=age)
    db.add(new_user)
    db.commit()
    return templates.TemplateResponse('register.html', {'request': request,
                                                        'success': "Пользователь успешно зарегистрирован"},
                                      status_code=201)


@router.post('/login')
# Авторизация пользователя
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    return {'status_code': status.HTTP_200_OK, 'transaction': f'Пользователь {username} успешно авторизован!!'}


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    # подключается к базе данных в момент обращения при помощи функции get_db
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )
    db.delete(user)
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Пользователь успешно удален!'}