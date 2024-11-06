from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from datetime import datetime, timedelta

import os
import jwt

client_id = os.getenv('CLIENT_ID', '')
client_secret = os.getenv('CLIENT_SECRET', '')
jwt_secret_key = os.getenv('JWT_SECRET_KEY', '')

router = APIRouter()
security = HTTPBearer()

async def verify_token(credentials: HTTPBasicCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail='Invalid authorization header')
    try:
        token = credentials.credentials
        payload = jwt.decode(token, jwt_secret_key, algorithms=['HS256'])
        return payload
    except:
        raise HTTPException(status_code=401, detail='Invalid token')

@router.post("/auth")
async def generate_token(credentials: HTTPBasicCredentials):
    if credentials.username == client_id and credentials.password == client_secret:
        expiration_time = datetime.utcnow() + timedelta(hours=2)  # Set expiration time to 2 hours from now
        payload = {
            "client_id": credentials.username,
            "exp": expiration_time
        }
        token = jwt.encode(payload, jwt_secret_key, algorithm='HS256')
        return {'access_token': token, 'token_type': 'bearer', "expires_in": expiration_time}
    else:
        raise HTTPException(status_code=401, detail='Invalid client_id or client_secret')
