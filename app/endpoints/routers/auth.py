from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app.endpoints.database import get_db
from app.endpoints.models import User
from app.endpoints.schemas import UserLogin
from app.endpoints import models, utils
from app.endpoints import oauth2
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(tags=["Authentication"])

class Authenticator:
    @router.post("/login")
    def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
        """
        Log in a user with provided credentials.

        Args:
            user_credentials (UserLogin): User credentials containing email and password.
            db (Session, optional): Database session. Defaults to Depends(get_db).

        Returns:
            dict: Token or other response upon successful login.
        """
        user = db.query(User).filter(User.email == user_credentials.email).first()
        if user is None or not utils.verify(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        
        access_token = oauth2.create_access_token(data={"user_id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}
    
