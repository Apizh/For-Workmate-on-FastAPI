import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Тестовая база данных SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


# Dependency override для использования тестовой БД
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# Тесты
@pytest.mark.asyncio
async def test_create_breed():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/breeds/", json={"name": "Persian"})
    assert response.status_code == 200
    assert response.json()["name"] == "Persian"


@pytest.mark.asyncio
async def test_get_breeds():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/breeds/")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.asyncio
async def test_create_kitten():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/kittens/", json={
            "name": "Mittens",
            "color": "Gray",
            "age_months": 4,
            "description": "Cute gray kitten",
            "breed_id": 1
        })
    assert response.status_code == 200
    assert response.json()["name"] == "Mittens"


@pytest.mark.asyncio
async def test_get_kittens():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/kittens/")
    assert response.status_code == 200
    assert len(response.json()) > 0
