from fastapi import FastAPI
from app.routes.generate import router

app = FastAPI(
    title="ArchitectAI",
    version="1.0"
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "ArchitectAI Backend Running 🚀"
    }