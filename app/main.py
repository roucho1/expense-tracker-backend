# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.routers import auth, transactions, categories

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://expense-tracker-frontend.vercel.app",  # 之後部署再換成正確網址
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])


@app.get("/")
def read_root():
    return {"message": "Expense Tracker API"}


@app.head("/")
def head_root():
    return {"message": "Expense Tracker API"}
