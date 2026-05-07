from fastapi import FastAPI
from app.routes import user, expense
from app.config.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(expense.router)

@app.get("/")
def root():
    return {"message:" "API Running"}