from database import engine
import models

def init_db():
    """Create database tables"""
    models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.") 