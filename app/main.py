from fastapi import FastAPI
from app.routers import user, book

app = FastAPI()  # Создаем экземпляр приложения FastAPI

app.include_router(user.router)
app.include_router(book.router)  # подключаем дополнительные внешние роутеры


# для запуска не из терминала, а напрямую
# if __name__ == "__main__":
#     uvicorn.run(app)
