from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models import search_similar_question, get_random_qna

app = FastAPI()

# Шаблоны для рендеринга HTML страниц
templates = Jinja2Templates(directory="app/templates")

# Главная страница с формой для ввода вопроса
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    random_qna = get_random_qna()
    return templates.TemplateResponse("index.html", {"request": request, "random_qna": random_qna})

# Эндпоинт для обработки формы с вопросом
@app.post("/search/", response_class=HTMLResponse)
async def post_search(request: Request, question: str = Form(...)):
    answer = search_similar_question(question)
    random_qna = get_random_qna()
    return templates.TemplateResponse("index.html", {"request": request, "answer": answer, "random_qna": random_qna})
