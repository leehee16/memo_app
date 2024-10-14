from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn


app = FastAPI()

# html 문서를 위한 객체
templates = Jinja2Templates(directory="templates")

# 정적파일을 위한 설정
## 정적파일(static) 종류(image, css, js)
app.mount("/staic", StaticFiles(directory="static"))

# localhost:8000/
@app.get("/")
async def home(request: Request):
    data = 100
    data2 = "fastapi 잘하고 싶다."
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "todos": data, "data2": data2}
        )

# python main.py
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

# CLI명령 : uvicorn main:app --reload