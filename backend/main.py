from fastapi import FastAPI
from db import init_db
from fastapi.middleware.cors import CORSMiddleware
from route import login, tasks

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(login.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to the list of domains that should be allowed to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
