from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel, Field, Session, create_engine, select
from pydantic import BaseModel
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
from collections import defaultdict

app = FastAPI(title="Millionaire Game")
DATABASE_URL = "sqlite:///millionaire.db"
engine = create_engine(DATABASE_URL, echo=True)

SECRET_KEY = "supersecretkey"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

user_progress = defaultdict(lambda: {"asked": [], "score": 0, "finished": False})

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    score: int = 0

class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str

    class Config:
        json_schema_serialization_defaults = {"by_alias": True, "title_case_keys": False, "sort_keys": False}

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class QuestionCreate(BaseModel):
    text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str

def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    preload_questions()

def preload_questions():
    with Session(engine) as session:
        count = len(session.exec(select(Question)).all())
        if count >= 10:
            return
        questions = [
            Question(text="Столица Франции?", option_a="Берлин", option_b="Мадрид", option_c="Париж", option_d="Рим", correct_option="c"),
            Question(text="Сколько континентов на Земле?", option_a="5", option_b="6", option_c="7", option_d="8", correct_option="c"),
            Question(text="Кто написал 'Война и мир'?", option_a="Пушкин", option_b="Толстой", option_c="Достоевский", option_d="Чехов", correct_option="b"),
            Question(text="Какой элемент обозначается как 'O'?", option_a="Кислород", option_b="Золото", option_c="Олово", option_d="Углерод", correct_option="a"),
            Question(text="Самая длинная река в мире?", option_a="Амазонка", option_b="Нил", option_c="Миссисипи", option_d="Янцзы", correct_option="a"),
            Question(text="Сколько дней в високосном году?", option_a="365", option_b="366", option_c="364", option_d="367", correct_option="b"),
            Question(text="Кто нарисовал 'Мону Лизу'?", option_a="Микеланджело", option_b="Рафаэль", option_c="Да Винчи", option_d="Ван Гог", correct_option="c"),
            Question(text="Какой газ необходим для дыхания?", option_a="Азот", option_b="Кислород", option_c="Углекислый газ", option_d="Гелий", correct_option="b"),
            Question(text="Сколько ног у паука?", option_a="6", option_b="8", option_c="10", option_d="12", correct_option="b"),
            Question(text="Какой океан самый большой?", option_a="Атлантический", option_b="Индийский", option_c="Северный Ледовитый", option_d="Тихий", correct_option="d"),
        ]
        session.add_all(questions)
        session.commit()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise credentials_exception
    return user

@app.post("/auth/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.username == user.username)).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(username=user.username, password=user.password)
    session.add(new_user)
    session.commit()
    return {"message": "User registered"}

@app.post("/auth/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not db_user or db_user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    return JSONResponse(content={"access_token": access_token, "token_type": "bearer"})

@app.get("/game/questions")
def get_questions(session: Session = Depends(get_session)):
    return session.exec(select(Question).limit(10)).all()

@app.post("/game/questions")
def add_question(q: QuestionCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    question = Question(**q.dict())
    session.add(question)
    session.commit()
    return {"message": f"Question added by {user.username}"}

@app.put("/game/questions/{question_id}")
def update_question(question_id: int, q: QuestionCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    for key, value in q.dict().items():
        setattr(question, key, value)
    session.commit()
    return {"message": f"Question updated by {user.username}"}

@app.get("/game/leaderboard")
def get_leaderboard(session: Session = Depends(get_session)):
    return session.exec(select(User).order_by(User.score.desc()).limit(10)).all()

@app.get("/game/play")
def play(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    progress = user_progress[user.id]
    if progress["finished"]:
        return {"message": "Игра завершена", "score": progress["score"]}

    asked_ids = progress["asked"]
    question = session.exec(select(Question).where(Question.id.not_in(asked_ids))).first()
    if not question:
        progress["finished"] = True
        return {"message": "Поздравляем! Вы ответили на все вопросы!", "score": progress["score"]}

    progress["asked"].append(question.id)
    return {
        "question_id": question.id,
        "text": question.text,
        "options": {
            "a": question.option_a,
            "b": question.option_b,
            "c": question.option_c,
            "d": question.option_d
        }
    }

@app.post("/game/answer")
async def answer(request: Request, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    data = await request.json()
    question_id = data.get("question_id")
    selected = data.get("selected_option")

    progress = user_progress[user.id]
    if progress["finished"]:
        return {"message": "Игра уже завершена", "score": progress["score"]}

    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    if selected == question.correct_option:
        progress["score"] += 1
        if progress["score"] >= 10:
            progress["finished"] = True
            user.score += 10
            session.add(user)
            session.commit()
            return {"message": "Вы выиграли миллион!", "score": 10}
        return {"message": "Верно!", "score": progress["score"]}
    else:
        progress["finished"] = True
        user.score += progress["score"]
        session.add(user)
        session.commit()
        return {"message": f"Неверно. Игра окончена. Ваш счёт: {progress['score']}"}

