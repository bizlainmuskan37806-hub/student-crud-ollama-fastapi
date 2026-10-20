from fastapi import FastAPI

from app.database import init_db
from app.routes import api_router

init_db()

app = FastAPI(
    title="Student CRUD API",
    description="SQLite student CRUD with Ollama llama3.2 answers for questions.",
    version="1.0.0",
)
app.include_router(api_router)


@app.get("/health")
def health():
    return {"status": "ok"}
