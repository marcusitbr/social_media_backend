from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if a plain password matches a hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        # Handle exceptions, such as invalid hashed password format or incorrect hashing algorithm
        print(f"Error verifying password: {e}")
        return False