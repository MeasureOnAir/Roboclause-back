from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from app.route import chat

app = FastAPI()
app.include_router(chat.router)

origins = [
    "http://localhost",
    "http://localhost:3000/*",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000/*",
    "http://127.0.0.1:8000/*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Roboclause!", "status": "🟢 Alive"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
