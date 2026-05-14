from itsdangerous import URLSafeSerializer
from passlib.context import CryptContext
from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
serializer = URLSafeSerializer(settings.SECRET_KEY)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_session(user_id: int) -> str:
    return serializer.dumps({"user_id": user_id})

def get_user_from_session(request: Request, db: Session = Depends(get_db)):
    session_token = request.cookies.get("session")
    if not session_token:
        return None
    try:
        data = serializer.loads(session_token)
        user_id = data.get("user_id")
        if not user_id:
            return None
        return db.query(User).filter(User.id == user_id).first()
    except Exception:
        return None

def login_required(user=Depends(get_user_from_session)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user
