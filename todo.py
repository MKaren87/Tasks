from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class TodoItem(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    completed: bool = False

todo_db = []

@app.post("/todos/")
async def create_todo(item: TodoItem):
    todo_id = len(todo_db) + 1
    todo = {'id': todo_id, **item.dict()}
    todo_db.append(todo)
    return todo

@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    for todo in todo_db:
        if todo['id'] == todo_id:
            return todo
    return {"error": "Todo item not found"}

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, item: TodoItem):
    for todo in todo_db:
        if todo['id'] == todo_id:
            todo.update(item.dict())
            return todo
    return {"error": "Todo item not found"}

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    global todo_db
    todo_db = [todo for todo in todo_db if todo['id'] != todo_id]
    return {"message": "Todo item deleted successfully"}

@app.get("/todos/")
async def list_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    q: Optional[str] = None,
    completed: Optional[bool] = None
):
    results = todo_db

    if q:
        results = [todo for todo in results if q.lower() in todo['title'].lower()]
    if completed is not None:
        results = [todo for todo in results if todo['completed'] == completed]

    return results[skip:skip+limit]

@app.put("/todos/{todo_id}/complete")
async def mark_todo_complete(todo_id: int):
    for todo in todo_db:
        if todo['id'] == todo_id:
            todo['completed'] = True
            return todo
    return {"error": "Todo item not found"}

class DescriptionUpdate(BaseModel):
    description: str

@app.patch("/todos/{todo_id}/description")
async def update_description(todo_id: int, desc: DescriptionUpdate):
    for todo in todo_db:
        if todo['id'] == todo_id:
            todo['description'] = desc.description
            return todo
    return {"error": "Todo item not found"}

