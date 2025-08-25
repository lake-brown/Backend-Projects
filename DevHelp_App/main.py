# main.py
from fastapi import FastAPI
from sqlalchemy.orm import Session

from database import engine, get_db
import models
from routers import users, questions, votes, auth  # auth is here

ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "adminpassword"

app = FastAPI(title="DevHelp App")

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(questions.router, prefix="/questions", tags=["Questions"])
app.include_router(votes.router, prefix="/votes", tags=["Votes"])

@app.on_event("startup")
def on_startup():
    # Create all tables
    models.Base.metadata.create_all(bind=engine)

    # Create default admin if not exists
    db: Session = next(get_db())

    admin = db.query(models.User).filter(models.User.email == ADMIN_EMAIL).first()
    if not admin:
        # Correct import path
        from routers.auth import get_password_hash
        new_admin = models.User(
            username="admin",
            email=ADMIN_EMAIL,
            hashed_password=get_password_hash(ADMIN_PASSWORD),
            role="admin"
        )
        db.add(new_admin)
        db.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")
