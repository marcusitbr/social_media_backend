from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from app.endpoints.schemas import Token, TokenData
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from jose import jwt
from app.endpoints import database




oauth2_sheme = OAuth2PasswordBearer(tokenUrl="login")

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    id: str = payload.get("user_id")

    if id is None:
        raise credentials_exception
    token_data = TokenData(id=id)

###################################################################################################

# Define a function named verify_access_token that takes two arguments:
# 1. token: a string representing the JWT token to be verified.
# 2. credentials_exception: an instance of HTTPException to be raised if token validation fails.
# The return type annotation specifies that the function returns an optional TokenData object.

def verify_access_token(token: str, credentials_exception: HTTPException) -> Optional[TokenData]:

    # Start a try-except block to handle potential exceptions during token decoding.

    try:
        # Decode the JWT token using the jwt.decode method.
        # The token is decoded using the provided SECRET_KEY and ALGORITHM.
        # The algorithms parameter specifies the allowed algorithms for decoding.
        # The decoded payload is stored in the payload variable.

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract the user_id from the decoded payload using the get method.
        # If user_id is not present in the payload, it will return None.

        user_id: str = payload.get("user_id")

        # Check if user_id is None.
        # If user_id is None, it indicates that the token is invalid or incomplete.
        # In such cases, raise the credentials_exception to indicate unauthorized access.

        if user_id is None:
            raise credentials_exception

        # If user_id is not None, create a TokenData object using the extracted user_id.
        # TokenData is a Pydantic model representing the decoded token data.
        # This object will be returned if the token is valid.

        token_data = TokenData(id=user_id)

        # Return the TokenData object containing the user_id.

        return token_data

    # Catch jwt.exceptions.DecodeError, which is raised when token decoding fails.
    # In case of a decode error, raise the credentials_exception to indicate unauthorized access.

    except jwt.exceptions.DecodeError:
        raise credentials_exception

    # Catch jwt.exceptions.ExpiredSignatureError, which is raised when the token has expired.
    # If the token has expired, return None to indicate that the token is no longer valid.

    except jwt.exceptions.ExpiredSignatureError:
        # Handle expired token (optional)
        return None

###################################################################################################



def get_current_user(token: str = Depends(oauth2_sheme)) -> TokenData:

    # Create an instance of HTTPException, which will be raised if credentials validation fails.
    # The status code is set to 401 UNAUTHORIZED, indicating that the user is not authenticated.
    # The detail message provides information about why the credentials could not be validated.
    # The headers specify the authentication method to be used (Bearer token).

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # Call the verify_access_token function with the token and credentials_exception as arguments.
    # This function verifies the provided token and returns the decoded token data (if valid).

    # return verify_access_token(token, credentials_exception)


###################################################################################################

# def get_current_user(token: str = Depends(oauth2_sheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"}
#     )
    # return verify_access_token(token)