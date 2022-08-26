from app.database.database import SessionLocal


class DbHandler:
    def __enter__(self):
       self.db = SessionLocal()
       return self.db
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.db.close()


def get_db():
    with DbHandler() as db:
        yield db