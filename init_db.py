from app.core.database import engine, Base
from app.models.models import User, Project, Chapter, Draft

def init_db():
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
