from fastapi import FastAPI
from sqlalchemy.orm import Session

from database import engine, get_db
import models
from routers import users, questions, votes, auth

from fastapi.middleware.cors import CORSMiddleware

ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "adminpassword"

# 1️⃣ Create the FastAPI app first
app = FastAPI(title="DevHelp App")

# 2️⃣ Add CORS middleware AFTER app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3️⃣ Include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(questions.router, prefix="/questions", tags=["Questions"])
app.include_router(votes.router, prefix="/votes", tags=["Votes"])

# 4️⃣ Startup event to create tables and admin
@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)

    db: Session = next(get_db())
    admin = db.query(models.User).filter(models.User.email == ADMIN_EMAIL).first()
    if not admin:
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
