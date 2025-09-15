import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

app = FastAPI(title="ToDo App with Raw SQL")

DB_NAME = "todos.db"

class Todo(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: Optional[datetime] = None

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

@app.on_event("startup")
def startup():
    init_db()

@app.post("/todos", response_model=Todo)
def create_todo(todo: Todo):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO todos (title, description, completed)
            VALUES (?, ?, ?)
        """, (todo.title, todo.description, todo.completed))
        todo.id = cursor.lastrowid
        cursor.execute("SELECT created_at FROM todos WHERE id = ?", (todo.id,))
        todo.created_at = cursor.fetchone()[0]
    return todo

@app.get("/todos", response_model=List[Todo])
def read_todos():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos")
        rows = cursor.fetchall()
        return [Todo(**dict(row)) for row in rows]

@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        return Todo(**dict(row))

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, new_data: Todo):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Задача не найдена")
        cursor.execute("""
            UPDATE todos
            SET title = ?, description = ?, completed = ?
            WHERE id = ?
        """, (new_data.title, new_data.description, new_data.completed, todo_id))
        conn.commit()
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        return Todo(**dict(zip([column[0] for column in cursor.description], row)))

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Задача не найдена")
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
    return {"message": "Задача удалена"}