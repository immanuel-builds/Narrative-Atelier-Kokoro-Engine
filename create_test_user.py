from app.core.database import SessionLocal
from app.models.models import User
from passlib.hash import bcrypt

def create_test_user():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "test@example.com").first()
        if not user:
            print("Creating test user...")
            hashed_password = bcrypt.hash("password123")
            user = User(
                username="testuser",
                email="test@example.com",
                password_hash=hashed_password
            )
            db.add(user)
            db.commit()
            print("Test user created.")
        else:
            print("Test user already exists.")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
