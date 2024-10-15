from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from database import Base, SessionLocal
import models
from database import Base, engine

app = FastAPI()

# DB 엔진 연결
Base.metadata.create_all(bind=engine)

# html 문서를 위한 객체
templates = Jinja2Templates(directory="templates")

# 정적파일을 위한 설정
## 정적파일(static) 종류(image, css, js)
app.mount("/static", StaticFiles(directory="static"), name="static")

# localhost:8000/
@app.get("/")
async def home(request: Request):
    # 비즈니스 로직 처리
    data = 100
    data2 = "fastapi 잘하고 싶다."
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "todos": data, "data2": data2}
        )

@app.post("/add")
async def add(request: Request, task: str = Form(...)):
    # 클라이언트에서 textarea에서 입력 데이터 넘어오면
    # db 테이블에 저장하고 결과를 html에 랜더링에서 리턴
    print(task)
    pass

# python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

# CLI명령 : uvicorn main:app --reload