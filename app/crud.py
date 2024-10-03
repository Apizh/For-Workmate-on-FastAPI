from sqlalchemy.orm import Session
from . import models, schemas


def get_breeds(db: Session):
    return db.query(models.Breed).all()


def get_kittens(db: Session):
    return db.query(models.Kitten).all()


def get_kitten(db: Session, kitten_id: int):
    return db.query(models.Kitten).filter(models.Kitten.id == kitten_id).first()


def create_kitten(db: Session, kitten: schemas.KittenCreate):
    db_kitten = models.Kitten(**kitten.dict())
    db.add(db_kitten)
    db.commit()
    db.refresh(db_kitten)
    return db_kitten


def update_kitten(db: Session, kitten_id: int, kitten: schemas.KittenCreate):
    db_kitten = get_kitten(db, kitten_id)
    if db_kitten:
        for key, value in kitten.dict().items():
            setattr(db_kitten, key, value)
        db.commit()
        db.refresh(db_kitten)
        return db_kitten
    return None


def delete_kitten(db: Session, kitten_id: int):
    db_kitten = get_kitten(db, kitten_id)
    if db_kitten:
        db.delete(db_kitten)
        db.commit()
        return db_kitten
    return None
