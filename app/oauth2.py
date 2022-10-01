from jose import JWTError, jwt
from datetime import datetime, timedelta

# secret key
# Algorithm
# expiration time

SECRET_KEY = "a403fcbdaaaf266f9d368757bd62e0bb6691fdd278c26a6ec9e13d5a2b17fae0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
