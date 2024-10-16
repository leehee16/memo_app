from sqlalchemy.orm import Session
import models

def get_todos(db: Session):
    return db.query(models.Todo).filter(models.Todo.completed == False).all()

def get_logs(db: Session):
    return db.query(models.Log).order_by(models.Log.completed_date.desc()).all()

def create_todo(db: Session, task: str):
    new_todo = models.Todo(task=task)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

def delete_todo(db: Session, todo_id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
    return todo

def complete_todo(db: Session, todo_id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo:
        todo.completed = True
        log = models.Log(todo_id=todo.id, task=todo.task)
        db.add(log)
        db.commit()
    return todo
