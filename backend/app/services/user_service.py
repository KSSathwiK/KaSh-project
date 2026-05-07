from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.hash import has_password

def create_user(db: Session, email:str, password: str):
    existing_user = get_user_by_email(db, email)
    
    if existing_user:
        return None
     
    new_user = User(
        email = email,
        password = has_password(password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()