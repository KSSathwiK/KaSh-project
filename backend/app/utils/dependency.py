from fastapi import Depends, HTTPException
from jose import jwt
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.user import User
import os
from dotenv import load_dotenv
# from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

security = HTTPBearer()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORTHM = os.getenv("ALGORITHM")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORTHM])
        user_id = payload.get("user_id")
    except:
        return HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.id == user_id).first()

    if not user: 
        raise HTTPException(status_code=401,detail="User not found")
    
    return user
