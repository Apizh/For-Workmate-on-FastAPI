from pydantic import BaseModel


class KittenBase(BaseModel):
    name: str
    color: str
    age_months: int
    description: str
    breed_id: int


class KittenCreate(KittenBase):
    pass


class Kitten(KittenBase):
    id: int
    breed: str

    class Config:
        orm_mode = True


class BreedBase(BaseModel):
    name: str


class BreedCreate(BreedBase):
    pass


class Breed(BreedBase):
    id: int

    class Config:
        orm_mode = True
