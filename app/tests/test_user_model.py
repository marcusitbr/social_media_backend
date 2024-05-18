import pytest
from sqlalchemy.orm import sessionmaker
from app.endpoints.database import engine, Base
# from app.endpoints.models import User
from datetime import datetime
from sqlalchemy.orm import Session
#from app.models import Post
# from app.endpoints.database import engine, get_db
# from app.endpoints import models
# from ..models.post import Post
from app.endpoints.models import GetPost, User
# from app.endpoints.database import SessionLocal, connect_to_database
# from app.endpoints.schemas import Post, PostCreate
# from app.endpoints.database import Base



SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_user(db):
    # Given
    user_data = {"username": "testuser", "email": "test@example.com", "password": "testpassword", "is_active": True, "created_at": datetime.now()}

    # When
    user = User(**user_data)
    db.add(user)
    db.commit()

    # Then
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.password == "testpassword"
    assert user.is_active is True
    assert user.created_at is not None
