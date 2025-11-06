import jwt
from datetime import datetime, timedelta


def encode_jwt(data, secret, algorithm="HS256", expire_hours=1):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=expire_hours)
    token = jwt.encode(payload, secret, algorithm=algorithm)
    return token


def decode_jwt(token, secret, algorithms=["HS256"]):
    payload = jwt.decode(token, secret, algorithms=algorithms)
    return payload
