from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Base, Kitten, Breed
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

# Создаем движок базы данных (например, для PostgreSQL)
DATABASE_URL = "postgresql://user:password@localhost/kittens_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Pydantic модели для валидации запросов
class KittenCreate(BaseModel):
    name: str
    age: int
    color: str
    description: str
    breed_id: int


class BreedCreate(BaseModel):
    name: str


# Зависимость для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Эндпоинт для получения списка всех пород
@app.get("/breeds/")
def get_breeds(db: Session = Depends(get_db)):
    return db.query(Breed).all()


# Эндпоинт для получения списка всех котят
@app.get("/kittens/")
def get_kittens(db: Session = Depends(get_db)):
    return db.query(Kitten).all()


# Эндпоинт для получения котят определенной породы
@app.get("/kittens/breed/{breed_id}")
def get_kittens_by_breed(breed_id: int, db: Session = Depends(get_db)):
    return db.query(Kitten).filter(Kitten.breed_id == breed_id).all()


# Эндпоинт для добавления нового котенка
@app.post("/kittens/")
def create_kitten(kitten: KittenCreate, db: Session = Depends(get_db)):
    db_kitten = Kitten(**kitten.dict())
    db.add(db_kitten)
    db.commit()
    db.refresh(db_kitten)
    return db_kitten
