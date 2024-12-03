from fastapi import FastAPI
from app.routers import user, book
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()  # Создаем экземпляр приложения FastAPI

app.include_router(user.router)
app.include_router(book.router)  # подключаем дополнительные внешние роутеры

templates = Jinja2Templates(directory='app/templates')


@app.get('/')
async def main(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})




# для запуска не из терминала, а напрямую
# if __name__ == "__main__":
#     uvicorn.run(app)
