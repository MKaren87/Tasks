from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    name: str = Field(..., description="Имя пользователя")
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    age: Optional[int] = Field(None, gt=0, description="Возраст (положительное целое число)")
    is_subscribed: Optional[bool] = Field(False, description="Подписан ли пользователь на рассылку")

app = FastAPI()

@app.post("/create_user")
async def create_user(user: UserCreate):
    return JSONResponse(content=user.dict())