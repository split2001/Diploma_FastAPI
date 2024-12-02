from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int


class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    age: int


class CreateBook(BaseModel):
    title: str
    description: str
    author: str
    genre: str
    completed: bool


class UpdateBook(BaseModel):
    title: str
    description: str
    author: str
    genre: str
    completed: bool
