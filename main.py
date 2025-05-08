# main.py (updated)
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from qa_system import qa_engine

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, question: str = None, answer: str = None):
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "question": question,
            "answer": answer
        }
    )

@app.post("/", response_class=HTMLResponse)
async def ask_question(request: Request, question: str = Form(...)):
    answer = qa_engine.ask(question)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "question": question,
            "answer": answer
        }
    )