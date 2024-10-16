from fastapi import FastAPI, Form, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from sqlalchemy.orm import Session
from database import Base, SessionLocal, engine
import models
from datetime import datetime

app = FastAPI()

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

# html 문서를 위한 객체
templates = Jinja2Templates(directory="templates")

# 정적파일을 위한 설정
## 정적파일(static) 종류(image, css, js)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 데이터베이스 세션 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# localhost:8000/
@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).filter(models.Todo.completed == False).all()
    logs = db.query(models.Log).order_by(models.Log.completed_date.desc()).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "todos": todos, "logs": logs}
    )

@app.post("/add")
async def add(task: str = Form(...), db: Session = Depends(get_db)):
    if task.strip() == "":
        raise HTTPException(status_code=400, detail="Task cannot be empty")
    try:
        new_todo = models.Todo(task=task)
        db.add(new_todo)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete/{todo_id}")
async def delete(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/complete/{todo_id}")
async def complete(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo:
        todo.completed = True
        log = models.Log(todo_id=todo.id, task=todo.task)
        db.add(log)
        db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.get("/edit/{todo_id}")
async def edit_form(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return templates.TemplateResponse("edit.html", {"request": request, "todo": todo})

@app.post("/edit/{todo_id}")
async def edit_todo(todo_id: int, task: str = Form(...), db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.task = task
    db.commit()
    return RedirectResponse(url="/", status_code=303)

# python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

# CLI명령 : uvicorn main:app --reload
