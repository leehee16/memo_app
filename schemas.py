from pydantic import BaseModel
from datetime import datetime

class TodoBase(BaseModel):
    task: str

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class LogBase(BaseModel):
    todo_id: int
    task: str

class Log(LogBase):
    id: int
    completed_date: datetime

    class Config:
        orm_mode = True
