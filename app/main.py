import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.utilities.db import create_db_and_tables
from app.routers.products.products import router as products_router

app = FastAPI(
    title="FastAPI Gunicorn Config",
    description="RESTful API for managing products",
    version="0.1.0",
    root_path=settings.root_path,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(products_router, tags=["products"], prefix="/api")

def on_starting(server):
    create_db_and_tables()


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )