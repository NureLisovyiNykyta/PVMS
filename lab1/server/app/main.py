from fastapi import FastAPI
import uvicorn
from app.api import string_controller
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Lab1 API",
    description="API to replace parentheses with square brackets in text.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(string_controller.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)