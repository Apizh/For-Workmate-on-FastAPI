from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/breeds/", response_model=list[schemas.Breed])
def read_breeds(db: Session = Depends(get_db)):
    return crud.get_breeds(db)


@app.get("/kittens/", response_model=list[schemas.Kitten])
def read_kittens(db: Session = Depends(get_db)):
    return crud.get_kittens(db)


@app.post("/kittens/", response_model=schemas.Kitten)
def create_kitten(kitten: schemas.KittenCreate, db: Session = Depends(get_db)):
    return crud.create_kitten(db, kitten)


@app.put("/kittens/{kitten_id}", response_model=schemas.Kitten)
def update_kitten(kitten_id: int, kitten: schemas.KittenCreate, db: Session = Depends(get_db)):
    db_kitten = crud.update_kitten(db, kitten_id, kitten)
    if db_kitten is None:
        raise HTTPException(status_code=404, detail="Kitten not found")
    return db_kitten


@app.delete("/kittens/{kitten_id}", response_model=schemas.Kitten)
def delete_kitten(kitten_id: int, db: Session = Depends(get_db)):
    db_kitten = crud.delete_kitten(db, kitten_id)
    if db_kitten is None:
        raise HTTPException(status_code=404, detail="Kitten not found")
    return db_kitten
