from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
import re

app = FastAPI()

feedbacks: List["Feedback"] = []

BANNED_WORDS = ["редиска", "бяка", "козявка"]

class Contact(BaseModel):
    email: EmailStr
    phone: Optional[str] = None

    @validator("phone")
    def validate_phone(cls, value):
        if value and not re.fullmatch(r"\d{7,15}", value):
            raise ValueError("Номер телефона должен содержать только цифры (7–15 символов)")
        return value

class Feedback(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    message: str = Field(..., min_length=10, max_length=500)
    contact: Contact

    @validator("message")
    def check_banned_words(cls, value):
        lowered = value.lower()
        for word in BANNED_WORDS:
            if re.search(rf"\b{word}\b", lowered):
                raise ValueError("Использование недопустимых слов")
        return value

@app.post("/feedback")
def submit_feedback(feedback: Feedback, is_premium: bool = Query(False)):
    feedbacks.append(feedback)

    response = f"Спасибо, {feedback.name}! Ваш отзыв сохранён."
    if is_premium:
        response += " Ваш отзыв будет рассмотрен в приоритетном порядке."

    return {"message": response}

