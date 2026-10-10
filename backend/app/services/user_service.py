from app.repositories.user_repository import get_user_by_email, save_user
from app.auth.service import hash_password, verify_password

def register_user(db, email: str, login: str, password: str):
    existing = get_user_by_email(db, email)

    if existing:
        raise Exception("User already exists")

    return save_user(db, email, login, hash_password(password))

def login_user(db, email: str, password: str):
    existing = get_user_by_email(db, email)

    if not existing:
        raise Exception("User not exists")
    
    if not verify_password(password, existing.password):
        raise Exception("Invalid password")
    
    return existing

